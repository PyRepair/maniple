### Analysis:
1. The buggy function `pivot_table` is recursively calling itself when `aggfunc` is a list. This recursive call leads to incorrect results and can cause an infinite loop.
2. The function fails when processing multi-index columns. The error message indicates that a `Series` object is being accessed with a `columns` attribute, which is not valid.
3. The failing test `test_pivot_table_multiindex_only` demonstrates the issue when calling `pivot_table` with multi-index columns.
4. The GitHub issue highlights the inconsistency and error in `pivot_table` behavior when using multi-index columns.

### Bug Cause:
The root cause of the bug lies in the recursive call of the `pivot_table` function when `aggfunc` is a list. Additionally, the incorrect handling of columns within the function results in the attribute error when processing multi-index columns.

### Bug Fix Strategy:
1. Remove the recursive call when `aggfunc` is a list to prevent an infinite loop.
2. Update the handling of columns to correctly process multi-index columns without raising an attribute error.

### Bug-fix implementation:
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
            agged = data.groupby(index + columns).agg(func)
            pieces.append(agged)
            keys.append(getattr(func, "__name__", func.__name__))

        return concat(pieces, keys=keys, axis=1)

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

        to_filter = [col for col in index + columns + values if col in data.columns]
        data = data[to_filter]

    else:
        values = data.columns
        values = [val for val in values if val not in keys]

    grouped = data.groupby(index + columns, observed=observed)
    agged = grouped.agg(aggfunc)
    if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
        agged = agged.dropna(how="all")

    table = agged

    if table.index.nlevels > 1:
        table = table.unstack()

    if not dropna and table.index.nlevels > 1:
        m = MultiIndex.from_arrays(
            cartesian_product(table.index.levels), names=table.index.names
        )
        table = table.reindex(m, axis=0)

    if isinstance(table, ABCDataFrame):
        table = table.sort_index(axis=1)

    if fill_value is not None:
        table = table._ensure_type(table.fillna(fill_value, downcast="infer"))

    if margins:
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

    if values_passed and not values_multi and not table.empty and (table.columns.nlevels > 1):
        table = table[values[0]]

    if len(index) == 0 and len(columns) > 0:
        table = table.T

    return table
```

By making these changes, the corrected `pivot_table` function will behave consistently with multi-index columns and avoid the recursive call issue.