### Bug Explanation:
The bug in the `pivot_table` function occurs when `aggfunc` is passed as a list. The function recursively calls itself with each function in the list, leading to unexpected behavior and incorrect results.

### Bug Fix Strategy:
To fix the bug, we need to handle the case where `aggfunc` is a list differently. Instead of recursively calling the function within the loop, we should iterate through the `aggfunc` list, calculate the pivot table for each function separately, and then concatenate the results together.

### Corrected Version of the `pivot_table` Function:
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
            agged = data.groupby(index + columns, observed=observed).agg(func)
            if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
                agged = agged.dropna(how="all")
            pieces.append(agged)
            keys.append(getattr(func, "__name__", func))

        return concat(pieces, keys=keys, axis=1)

    keys = index + columns

    # Rest of the function remains unchanged
```

By making this change, the `pivot_table` function should now handle multiple aggregation functions correctly when `aggfunc` is a list, passing the failing test cases and producing the expected results.