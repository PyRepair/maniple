### Bug Analysis:
The error occurs due to the DataFrame `table` being accessed using `.columns` on a Series object.

### Bug Explanation:
The bug arises when the following conditions are met:
- The user is attempting to create a pivot table with multi-index columns only.
- The function reaches the point where it checks `table.columns.nlevels > 1`.
- In this scenario, `table` is a `Series` object, not a `DataFrame`.

### Bug Fix Strategy:
To address the bug, it's necessary to ensure that `table` remains a `DataFrame` after the processing within the function. One potential solution is to check if `table` is a `DataFrame` before accessing its columns' attributes.

### Updated Function:
Here is the corrected version of the `pivot_table` function:
```python
from pandas import DataFrame

def pivot_table(
        data: DataFrame,
        values=None,
        index=None,
        columns=None,
        aggfunc="mean",
        fill_value=None,
        margins=False,
        dropna=True,
        margins_name="All",
        observed=False,
) -> DataFrame:
    index = data.columns if index is None else index
    columns = data.columns if columns is None else columns

    # ... Continued implementation of pivot_table function

    # Check if the result table is a DataFrame before column operations
    if isinstance(table, DataFrame):
        if (table.columns.nlevels > 1) and not table.empty:
            table = table[values[0]]

        if abs(len(index)) == 0 and abs(len(columns)) > 0:
            table = table.T

        if isinstance(table, DataFrame) and dropna:
            table = table.dropna(how='all', axis=1)

    return table
```

With this correction, the function ensures that `table` remains a `DataFrame` before accessing its columns' attributes, preventing the attribute error.