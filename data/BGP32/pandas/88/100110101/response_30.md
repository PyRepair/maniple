### Bug Explanation
The bug in the `pivot_table` function revolves around how the function handles multi-index columns. When the `columns` parameter contains more than one value (i.e., a tuple), the function fails to correctly process and operate on the multi-index columns. This results in the function returning a `Series` object instead of a `DataFrame`, leading to an attribute error when trying to access the `columns`.

### Bug Fix Strategy
To fix this bug, we need to ensure that the function correctly handles multi-index columns when constructing the resulting table and avoids the erroneous conversion of the table into a Series. We need to refactor the logic related to multi-index processing in the `pivot_table` function to correctly generate and return the DataFrame with multi-index columns intact.

### Corrected Function
Here is the corrected version of the `pivot_table` function:

```python
def pivot_table(
    data,
    values=None,
    index=None,
    columns=None,
    aggfunc="mean",
    fill_value=None,
    margins=False,
    dropna=True,
    margins_name="All",
    observed=False,
) -> "DataFrame":
    index = _convert_by(index)
    columns = _convert_by(columns)

    if isinstance(aggfunc, list):
        pieces: List[DataFrame] = []
        keys = []
        for func in aggfunc:
            table = pivot_table(
                data,
                values=values,
                index=index,
                columns=columns,
                fill_value=fill_value,
                aggfunc=func,
                margins=margins,
                dropna=dropna,
                margins_name=margins_name,
                observed=observed,
            )
            pieces.append(table)
            keys.append(getattr(func, "__name__", func))

        return concat(pieces, keys=keys, axis=1)

    keys = index + columns

    values_passed = values is not None
    # Handle simpler value input
    if values_passed:
        values = [values] if not is_list_like(values) else values

    # Make sure all value labels are present in data
    for val in values:
        if val not in data:
            raise KeyError(val)

    to_filter = [x.key if isinstance(x, Grouper) else x for x in keys + values]
    selected_columns = [x for x in to_filter if x in data]

    if len(selected_columns) < len(data.columns):
        data = data[selected_columns]

    grouped = data.groupby(keys, observed=observed)
    agged = grouped.agg(aggfunc)
    
    if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
        agged = agged.dropna(how="all")

    for value_label in values:
        if (
            value_label in data
            and is_integer_dtype(data[value_label])
            and value_label in agged
            and not is_integer_dtype(agged[value_label])
        ):
            agged[value_label] = maybe_downcast_to_dtype(agged[value_label], data[value_label].dtype)

    table = agged

    if table.index.nlevels > 1:
        table = table.unstack(range(len(index), len(keys))

    if not dropna:
        if table.index.nlevels > 1:
            m = MultiIndex.from_product(table.index.levels, names=table.index.names)
            table = table.reindex(m, axis=0)

        if table.columns.nlevels > 1:
            m = MultiIndex.from_product(table.columns.levels, names=table.columns.names)
            table = table.reindex(m, axis=1)

    if isinstance(table, ABCDataFrame):
        table = table.sort_index(axis=1)

    if fill_value is not None:
        table = table.fillna(fill_value)

    if margins:
        if dropna:
            data = data.dropna()
        table = _add_margins(
            table,
            data,
            values,
            rows=index,
            cols=columns,
            aggfunc=aggfunc,
            observed=True,
            margins_name=margins_name,
            fill_value=fill_value,
        )

    if values_passed and len(values) == 1 and table.columns.nlevels > 1:
        table = table[values[0]]

    if not index and columns:
        table = table.T

    if isinstance(table, ABCDataFrame) and dropna:
        table = table.dropna(how="all", axis=1)

    return table
```

By modifying the multi-index handling mechanism and ensuring that the function returns a DataFrame with multi-index columns appropriately preserved, the corrected `pivot_table` function should now pass the failing test cases provided.