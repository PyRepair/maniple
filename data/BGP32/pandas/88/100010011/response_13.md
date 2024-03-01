### Bug Analysis:
The bug occurs when using `pivot_table` with multi-index columns only. This results in an `AttributeError` because the `table` variable is inferred as a `Series` object and the `table` object being referenced with `table.columns.nlevels` results in the AttributeError.

### Bug Location:
The bug is located in the `pivot_table` function, specifically in the condition where it checks for the number of levels in columns (`table.columns.nlevels`). The bug originates from that point because it makes the assumption that `table` refers to a DataFrame, but in some cases, it can be a Series (when only multi-index columns are provided).

### Bug Explanation:
When the `pivot_table` function is called with multi-index columns, the resulting `table` after aggregation is inferred as a Series rather than a DataFrame. As a result, trying to access `table.columns` raises an AttributeError because a Series object does not have a `columns` attribute.

### Fix Strategy:
To fix the bug, the logic in the `pivot_table` function needs to be adjusted to handle the case where `table` is a Series, rather than a DataFrame. If `table` is a Series, the code should handle it appropriately to make the necessary checks or attributes access.

### Correction:

Here is the corrected version of the `pivot_table` function:

```python
def pivot_table(data, values=None, index=None, columns=None, aggfunc="mean", fill_value=None, margins=False, dropna=True, margins_name="All", observed=False) -> "DataFrame":
    index = _convert_by(index)
    columns = _convert_by(columns)

    if isinstance(aggfunc, list):
        pieces: List[DataFrame] = []
        keys = []
        for func in aggfunc:
            table = pivot_table(data, values=values, index=index, columns=columns, fill_value=fill_value, aggfunc=func, margins=margins, dropna=dropna, margins_name=margins_name, observed=observed)
            pieces.append(table)
            keys.append(getattr(func, "__name__", func))

        return concat(pieces, keys=keys, axis=1)

    keys = index + columns

    values_passed = values is not None
    if values_passed:
        if is_list_like(values):
            values_multi = True
            values = list(values)
        else:
            values_multi = False
            values = [values]

        # GH14938 Make sure value labels are in data
        for i in values:
            if i not in data:
                raise KeyError(i)

        to_filter = []
        for x in keys + values:
            if isinstance(x, Grouper):
                x = x.key
            try:
                if x in data:
                    to_filter.append(x)
            except TypeError:
                pass
        if len(to_filter) < len(data.columns):
            data = data[to_filter]

    else:
        values = data.columns
        for key in keys:
            try:
                values = values.drop(key)
            except (TypeError, ValueError, KeyError):
                pass
        values = list(values)

    grouped = data.groupby(keys, observed=observed)
    agged = grouped.agg(aggfunc)

    if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
        agged = agged.dropna(how="all")
        
    if isinstance(agged, ABCSeries):  # Handle case where agged is a Series
        agged = agged.to_frame()  # Convert Series to DataFrame for consistency

    for v in values:
        if v in data and is_integer_dtype(data[v]) and v in agged and not is_integer_dtype(agged[v]):
            agged[v] = maybe_downcast_to_dtype(agged[v], data[v].dtype)

    table = agged

    if dropna:    
        if table.index.nlevels > 1:
            m = MultiIndex.from_arrays(cartesian_product(table.index.levels), names=table.index.names)
            table = table.reindex(m, axis=0)

        if table.columns.nlevels > 1:
            m = MultiIndex.from_arrays(cartesian_product(table.columns.levels), names=table.columns.names)
            table = table.reindex(m, axis=1)
    
    if isinstance(table, ABCDataFrame):
        table = table.sort_index(axis=1)

    if fill_value is not None:
        table = table.fillna(fill_value)
    
    if margins:
        if dropna:
            data = data[data.notna().all(axis=1)]
        table = _add_margins(table, data, values, rows=index, cols=columns, aggfunc=aggfunc, observed=dropna, margins_name=margins_name, fill_value=fill_value)
        
    if values_passed and not values_multi and not table.empty and isinstance(table, ABCDataFrame) and (table.columns.nlevels > 1):
        table = table[values[0]]

    if len(index) == 0 and len(columns) > 0:
        table = table.T
        
    if isinstance(table, ABCDataFrame) and dropna:
        table = table.dropna(how="all", axis=1)

    return table
```

After applying the correction above, the `pivot_table` function should no longer throw an AttributeError when called with multi-index columns only.