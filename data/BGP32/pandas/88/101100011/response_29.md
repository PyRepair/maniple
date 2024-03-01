### Analysis:
- The buggy function `pivot_table` in the `pandas.core.reshape.pivot.py` file is intended to pivot table data like the `pivot_table` function in Pandas.
- The function seems to have a bug when handling multi-index columns only, as reported in the GitHub issue.
- The issue seems to arise when the `table` variable is a `Series` instead of a `DataFrame`, leading to an `AttributeError` when trying to access `columns`. This happens when the function is used for pivoting with multi-index columns only.

### Bug Explanation:
- The bug in the `pivot_table` function occurs when the aggregation results in a single-dimensional `Series` instead of a two-dimensional `DataFrame`. This leads to the wrong handling of the columns in the subsequent code.
- The error specifically occurs at `table.columns.nlevels > 1` when `table` is not a `DataFrame` but a `Series`.

### Bug Fix Strategy:
- To fix the bug, we need to ensure that the `table` variable is always a `DataFrame` even when the aggregation results in a single row or column.
- We can modify the logic to ensure that even for a single row or column result, the output is a `DataFrame` with appropriate index/column labels for single/multi-index cases.

### Correction:
```python
def pivot_table(data, values=None, index=None, columns=None, aggfunc='mean', fill_value=None, margins=False, dropna=True, margins_name='All', observed=False) -> 'DataFrame':
    # Body implementation remains the same, just add the following correction

    table = pd.DataFrame(agged) if not isinstance(agged, pd.DataFrame) else agged
```

By ensuring that `table` is always a `DataFrame`, we can avoid the `AttributeError` when trying to access `columns` on a `Series`. This correction should address the bug mentioned in the GitHub issue and make the function work correctly with multi-index columns only.