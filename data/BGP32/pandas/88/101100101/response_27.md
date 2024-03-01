## Bug Explanation
The bug occurs in the `pivot_table` function when calling itself recursively to handle cases where `aggfunc` is a list of functions. The issue arises because the function aggregates the data for each function separately but returns the result in a concatenated format with keys assigned, which is incorrect.

## Bug Fix
To fix the bug, we need to modify the section of code that handles the case where `aggfunc` is a list of functions. Instead of concatenating the results with keys, we should return a list of DataFrames, one for each function, in the correct order.

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

        return pieces

    keys = index + columns

    # Rest of the original function remains unchanged
```

With this fix, the function should now correctly handle the case where `aggfunc` is a list of functions.