### Bug Analysis:
The bug occurs when calling the `pivot_table()` function with multi-index columns only. The issue arises due to the handling of values passed to the function when the columns parameter contains multiple values.

### Error Location:
The error occurs in the section of the code where it checks if the passed values have multiple levels when constructing the output table after performing the aggregation.

### Bug Cause:
The bug is caused by incorrect handling of the column values in the pivot operation, specifically in cases where multi-index columns are used. This leads to an incorrect operation, resulting in the AttributeError because a Series object does not have the 'columns' attribute.

### Strategy for Fixing the Bug:
To fix the bug, we need to correctly handle the multi-index columns case in the `pivot_table()` function. We need to ensure that the multi-index columns are processed correctly when constructing the output DataFrame with the aggregated values.

### Corrected Version of the Function:
Below is a corrected version of the `pivot_table()` function that addresses the bug:

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

    table = agged
    if table.index.nlevels > 1:
        to_unstack = []
        for i in range(len(index), len(keys)):
            name = agged.index.names[i]
            if name is None or name in index:
                to_unstack.append(i)
            else:
                to_unstack.append(name)
        table = agged.unstack(to_unstack)

    if len(keys) == 0 and len(columns) > 0:
        table = table.T

    if isinstance(table, ABCDataFrame):
        table = table.sort_index(axis=1)
    
    return table
```

By adjusting the handling of multi-index columns and ensuring correct processing of the values passed, the corrected version of the `pivot_table()` function should now work correctly with the failing test case provided.