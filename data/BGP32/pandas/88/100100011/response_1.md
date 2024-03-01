### Bug Analysis:
- The buggy function is `pivot_table` from `pandas.core.reshape.pivot.py`.
- The bug occurs when trying to pivot a DataFrame with multi-index columns only.
- When attempting to pivot with multi-index columns only, the function fails with an `AttributeError`, `'Series' object has no attribute 'columns'`.
- The failing test function `test_pivot_table_multiindex_only` in `test_pivot.py` triggers this bug by attempting to pivot a DataFrame with multi-index columns only.

### Bug Details:
- The bug arises from the assumption that the input DataFrame will always have multi-index rows to pivot at the index and columns. When the DataFrame only has multi-index columns, it mistakenly treats 'table' as a Series object instead of a DataFrame, causing the AttributeError.

### Strategy for Bug Fix:
- To fix the bug, we need to ensure that even when the input DataFrame has only multi-index columns, the function correctly handles it as a DataFrame.
- We need to check for which axis we have multi-index labels and appropriately pivot the DataFrame.

### Bug Fix:

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

    if not index:  # Handle case when index is empty while columns have values
        index = data.index

    if not columns:  # Handle case when columns is empty while index has values
        columns = data.columns

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

    ...

    return table
```

### Summary:
- The bug was caused by the failure of the `pivot_table` function to handle the case of pivoting a DataFrame with multi-index columns only.
- The fix involves checking for empty index or columns and setting them to the proper DataFrame attributes to prevent the function from treating the data incorrectly.
- After the bug fix, the function should handle the pivoting of DataFrames correctly, even with multi-index columns only, resolving the issue reported on GitHub.