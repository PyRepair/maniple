### Bug Explanation:
The bug occurs when the function calls itself recursively to handle multiple aggregation functions provided as a list. In this case, the function is called with the same arguments resulting in an infinite loop. This leads to stack overflow and causes the function to fail.

### Fix Strategy:
To fix the bug, we need to modify the logic so that when `aggfunc` is a list, the function iterates through each function without calling itself recursively. Instead, it should perform the aggregation separately for each function and combine the results at the end.

### Corrected Version:
```python
def pivot_table(data, values=None, index=None, columns=None, aggfunc="mean", fill_value=None,
                margins=False, dropna=True, margins_name="All", observed=False) -> 'DataFrame':
    index = _convert_by(index)
    columns = _convert_by(columns)

    if isinstance(aggfunc, list):
        pieces: List[DataFrame] = []
        keys = []
        for func in aggfunc:
            grouped = data.groupby(keys, observed=observed)
            agged = grouped.agg(func)
            pieces.append(agged)
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

    if table.index.nlevels > 1:
        # Related GH #17123
        # If index_names are integers, determine whether the integers refer
        # to the level position or name.
        index_names = agged.index.names[: len(index)
        ...
        
    return table
```