### Issue:
The `pivot_table` function is calling itself recursively when the `aggfunc` parameter is a list, which results in an infinite loop, consuming an excessive amount of stack space and causing a stack overflow error. This recursion happens when iterating over multiple aggregation functions in the `aggfunc` list, leading to repeated calls to the same function with the same parameters.

### Fix Strategy:
To fix this issue, we need to prevent the function from calling itself recursively when `aggfunc` is a list. Instead, we should process each function in the list individually without invoking recursive calls.

### Corrected Code:
Below is the corrected version of the `pivot_table` function:

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
        pieces: List[DataFrame] = []
        keys = []

        for func in aggfunc:
            grouped = data.groupby(index + columns, observed=observed)
            agged = grouped.agg(func)
            if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
                agged = agged.dropna(how="all")

                for v in data.columns:
                    if v in agged and is_integer_dtype(data[v]) and not is_integer_dtype(agged[v]):
                        agged[v] = maybe_downcast_to_dtype(agged[v], data[v].dtype)

            table = agged
            if table.index.nlevels > 1:
                index_names = table.index.names[: len(index)]
                to_unstack = []
                for i in range(len(index), len(index) + len(columns)):
                    name = table.index.names[i]
                    if name is None or name in index_names:
                        to_unstack.append(i)
                    else:
                        to_unstack.append(name)
                table = table.unstack(to_unstack)

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
    if table.index.nlevels > 1:
        index_names = table.index.names[: len(index)]
        to_unstack = []
        for i in range(len(index), len(index) + len(columns)):
            name = table.index.names[i]
            if name is None or name in index_names:
                to_unstack.append(i)
            else:
                to_unstack.append(name)
        table = table.unstack(to_unstack)

    if not dropna:
        if table.index.nlevels > 1:
            table = table.reindex(cartesian_product(table.index.levels)).sort_index()
        if table.columns.nlevels > 1:
            table = table.reindex(cartesian_product(table.columns.levels), axis=1).sort_index()

    if fill_value is not None:
        table = table.fillna(fill_value)

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

    if values_passed and not values_multi and not table.empty:
        table = table[values[0].name]

    if not index and columns:
        table = table.T

    if isinstance(table, ABCDataFrame) and dropna:
        table = table.dropna(how="all", axis=1)

    return table
```

### Explanation:
In the corrected code, when processing multiple aggregation functions provided as a list in the `aggfunc` parameter, each function is applied sequentially without calling `pivot_table` recursively. This modification prevents the infinite loop issue. Additionally, the code has been adjusted to handle the processing logic as expected for multiple aggregation functions.