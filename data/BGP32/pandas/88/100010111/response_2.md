### Bug Analysis
The bug occurs when the `pivot_table` function is called with multi-index columns only, instead of a combination of index and columns. The issue arises when attempting to access the columns attribute of a Series object, leading to an AttributeError.

### Bug Location
The bug is in the return statement: `and (table.columns.nlevels > 1)`. In this case, `table` is a Series object because a specific configuration leads to returning a Series instead of a DataFrame.

### Explanation of the Bug
1. The `pivot_table` function is recursively called in:
   ```python
   table = pivot_table(data, values=values, index=index, columns=columns, fill_value=fill_value, aggfunc=func, margins=margins, dropna=dropna, margins_name=margins_name, observed=observed)
   ```
   This call creates a situation where a Series is returned when multiple aggfuncs are provided.
2. The return statement expecting the table to have `columns` attribute works fine for DataFrame but fails for Series. This is the cause of the AttributeError.

### Bug Fix Strategy
To fix this bug, a check should be added to determine the type of the `table` variable and handle Series and DataFrame objects differently. The goal is to ensure that even for cases where multiple aggfuncs are provided, the code properly handles multi-index columns.

### Code Fix
Here is the corrected version of the `pivot_table` function:
```python
def pivot_table(data, values=None, index=None, columns=None, aggfunc="mean", fill_value=None, margins=False, dropna=True, margins_name="All", observed=False) -> DataFrame:
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

        for v in values:
            if v in data and is_integer_dtype(data[v]) and v in agged and not is_integer_dtype(agged[v]):
                agged[v] = maybe_downcast_to_dtype(agged[v], data[v].dtype)

    table = agged
    if isinstance(table, ABCDataFrame):
        table = table.sort_index(axis=1)

    if fill_value is not None:
        table = table._ensure_type(table.fillna(fill_value, downcast="infer"))

    if margins:
        if dropna:
            data = data[data.notna().all(axis=1)]
        table = _add_margins(table, data, values, rows=index, cols=columns, aggfunc=aggfunc, observed=dropna, margins_name=margins_name, fill_value=fill_value)

    if values_passed and not values_multi and not table.empty and isinstance(table, ABCDataFrame) and table.columns.nlevels > 1:
        table = table[values[0]]

    if len(index) == 0 and len(columns) > 0:
        table = table.T

    if isinstance(table, ABCDataFrame) and dropna:
        table = table.dropna(how="all", axis=1)

    return table
``` 

This corrected version of the `pivot_table` function handles the situation with multi-index columns properly, ensuring that both DataFrame and Series objects are handled correctly according to the specific conditions.