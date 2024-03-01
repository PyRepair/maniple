### Bug Analysis
The bug occurs in the `pivot_table` function when using multi-index columns. The failing test cases demonstrate that when trying to pivot a DataFrame with multi-index columns, the function encounters an `AttributeError` due to the incorrect handling of series in the program flow.

### Bug Explanation
- The function attempts to pivot the DataFrame in cases where columns are multi-level indices.
- The program uses `table.columns.nlevels` to check if the columns of the pivoted table have more than one level.
- When `values_passed` is `True`, and the conditions for indexing properly into the DataFrame are met, the function tries to access the columns' levels.
- However, if the DataFrame is from the initial pivot, it could only have one level, turning it into a Series, and Series objects do not have a `columns` attribute. This leads to the `AttributeError`.

### Proposed Fix
A potential strategy to fix the bug involves adding a conditional check before accessing the `nlevels` property of `table.columns`. If `table` is a Series object, the function should operate differently to avoid the Attribute Error.

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

        # gh-21133
        # we want to down cast if
        # the original values are ints
        # as we grouped with a NaN value
        # and then dropped, coercing to floats
        for v in values:
            if (
                v in data
                and is_integer_dtype(data[v])
                and v in agged
                and not is_integer_dtype(agged[v])
            ):
                agged[v] = maybe_downcast_to_dtype(agged[v], data[v].dtype)

    table = agged

    if isinstance(table, ABCDataFrame) and not table.empty:
        if table.index.nlevels > 1:
            # Related GH #17123
            # If index_names are integers, determine whether the integers refer
            # to the level position or name.
            index_names = agged.index.names[: len(index)]
            to_unstack = []
            for i in range(len(index), len(keys)):
                name = agged.index.names[i]
                if name is None or name in index_names:
                    to_unstack.append(i)
                else:
                    to_unstack.append(name)
            table = agged.unstack(to_unstack)

        if not dropna:
            if table.index.nlevels > 1:
                m = MultiIndex.from_arrays(
                    cartesian_product(table.index.levels), names=table.index.names
                )
                table = table.reindex(m, axis=0)

            if table.columns.nlevels > 1:
                m = MultiIndex.from_arrays(
                    cartesian_product(table.columns.levels),
                    names=table.columns.names
                )
                table = table.reindex(m, axis=1)

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

    # discard the top level
    if (
        values_passed
        and not values_multi
        and not table.empty
        and hasattr(table, "columns")
        and table.columns.nlevels > 1
    ):
        table = table[values[0]]

    if len(index) == 0 and len(columns) > 0:
        table = table.T

    if isinstance(table, ABCDataFrame) and dropna:
        table = table.dropna(how="all", axis=1)

    return table
``` 

This corrected version of the function should now handle multi-index column cases appropriately and avoid triggering the AttributeError encountered in the failing test cases.