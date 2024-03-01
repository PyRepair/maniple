### Bug Analysis
The bug in the `pivot_table` function arises from recursive calls within the function. When the `aggfunc` parameter is a list of functions, the function tries to pivot the table for each function in the list. However, during this process, each call internally triggers another call to `pivot_table`, leading to unexpected behavior and incorrect outputs.

### Bug Explanation
1. In the failing test cases, the `pivot_table` function is called with a list of `aggfunc` containing multiple elements. For example, `aggfunc=["mean", "sum"]`.
2. Inside the `pivot_table` function, there is a check that identifies a list of `aggfunc` and then iterates over the list, calling `pivot_table` for each function in the list without proper handling of the recursive calls.
3. The recursive calls with list `aggfunc` lead to duplicated columns in the resulting DataFrame, which causes the test cases to fail.

### Bug Fix Strategy
To fix this bug, we need to remove the recursion within the `pivot_table` function when handling a list of `aggfunc`. Instead of recursively calling `pivot_table` again for each function in the `aggfunc` list, we should complete the pivot operation within the loop itself and correctly handle the aggregation for each function.

### Corrected Function
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
            grouped = data.groupby(index + columns, observed=observed)
            agged = grouped.agg(func)
            if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
                agged = agged.dropna(how="all")

                for v in values:
                    if (
                        v in data
                        and is_integer_dtype(data[v])
                        and v in agged
                        and not is_integer_dtype(agged[v])
                    ):
                        agged[v] = maybe_downcast_to_dtype(agged[v], data[v].dtype)

            table = agged
            if table.index.nlevels > 1:
                index_names = table.index.names[: len(index)]
                to_unstack = []
                for i in range(len(index), len(index) + len(columns)):
                    to_unstack.append(i)
                table = table.unstack(to_unstack)

            if not dropna:
                if table.index.nlevels > 1:
                    m = MultiIndex.from_arrays(
                        cartesian_product(table.index.levels), names=table.index.names
                    )
                    table = table.reindex(m, axis=0)

                if table.columns.nlevels > 1:
                    m = MultiIndex.from_arrays(
                        cartesian_product(table.columns.levels), names=table.columns.names
                    )
                    table = table.reindex(m, axis=1)

            if isinstance(table, ABCDataFrame):
                table = table.sort_index(axis=1)

            if fill_value is not None:
                table = table._ensure_type(table.fillna(fill_value, downcast="infer"))

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

        for i in values:
            if i not in data:
                raise KeyError(i)

        to_filter = [x.key if isinstance(x, Grouper) else x for x in keys + values]
        data = data[to_filter]

    else:
        values = data.columns
        for key in keys:
            values = values.drop(key, errors="ignore")
        values = list(values)

    grouped = data.groupby(keys, observed=observed)
    agged = grouped.agg(aggfunc)
    if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
        agged = agged.dropna(how="all")

        for v in values:
            if (
                v in data
                and is_integer_dtype(data[v])
                and v in agged
                and not is_integer_dtype(agged[v])
            ):
                agged[v] = maybe_downcast_to_dtype(agged[v], data[v].dtype)

    table = agged
    if table.index.nlevels > 1:
        index_names = table.index.names[: len(index)]
        to_unstack = []
        for i in range(len(index), len(len(keys))):
            to_unstack.append(i)
        table = table.unstack(to_unstack)

    if not dropna:
        if table.index.nlevels > 1:
            m = MultiIndex.from_arrays(
                cartesian_product(table.index.levels), names=table.index.names
            )
            table = table.reindex(m, axis=0)

        if table.columns.nlevels > 1:
            m = MultiIndex.from_arrays(
                cartesian_product(table.columns.levels), names=table.columns.names
            )
            table = table.reindex(m, axis=1)

    if isinstance(table, ABCDataFrame):
        table = table.sort_index(axis=1)

    if fill_value is not None:
        table = table._ensure_type(table.fillna(fill_value, downcast="infer"))

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

The corrected function now properly handles the case where `aggfunc` is a list of functions, ensuring that the pivot operation is performed for each function without triggering unnecessary recursive calls.