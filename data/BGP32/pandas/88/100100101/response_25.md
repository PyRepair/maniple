### Bug Explanation
The bug in the `pivot_table` function arises when the `aggfunc` parameter is a list of aggregation functions. In this case, the function recursively calls itself for each function in the list but does not properly handle the keys, resulting in incorrect behavior and an infinite loop.

### Bug Fix Strategy
To fix the bug, we need to ensure that when `aggfunc` is a list, the function correctly handles the keys for each aggregation function and properly concatenates the resulting tables.

### Corrected Function
```python
@Substitution("\ndata : DataFrame")
@Appender(_shared_docs["pivot_table"], indents=1)
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
        keys = index + columns
        pieces = []
        for func in aggfunc:
            table = pivot_table(
                data=data,
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

        return concat(pieces, keys=keys, axis=1)

    values_passed = values is not None
    if values_passed:
        if is_list_like(values):
            values_multi = True
            values = list(values)
        else:
            values_multi = False
            values = [values]

        for i in values:
            if i not in data:
                raise KeyError(i)

        to_filter = [x for x in keys + values if isinstance(x, str) and x in data]
        data = data[to_filter]

    else:
        values = data.columns
        values = [v for v in values if v not in keys]

    grouped = data.groupby(keys, observed=observed)
    agged = grouped.agg(aggfunc)

    if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
        agged = agged.dropna(how="all")

    table = agged

    if table.index.nlevels > 1:
        index_names = agged.index.names[: len(index)]
        to_unstack = [i for i in range(len(index), len(keys) + len(columns)) if agged.index.names[i] not in index_names]
        table = agged.unstack(to_unstack)

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
        table = table.fillna(fill_value, axis=0)

    if margins:
        if dropna:
            data = data[data.notna().all(axis=1)]
        table = _add_margins(
            table,
            data,
            values,
            rows=index,
            cols=columns,
            aggfunc=aggfunc,
            observed=dropna,
            margins_name=margins_name,
            fill_value=fill_value,
        )

    if values_passed and not values_multi and not table.empty and table.columns.nlevels > 1:
        table = table[values[0]]

    if len(index) == 0 and len(columns) > 0:
        table = table.T

    if isinstance(table, ABCDataFrame) and dropna:
        table = table.dropna(how="all", axis=1)

    return table
``` 

By incorporating the fixes described above, the corrected `pivot_table` function should now pass the failing test cases and provide the expected output values and types.