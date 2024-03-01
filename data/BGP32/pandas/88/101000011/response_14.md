### Analysis:
The bug occurs when calling the `pivot_table` function with `columns` as a multi-level index. This triggers an issue related to handling multi-level columns resulting in an AttributeError.

### Bug Location:
The bug occurs in the following section of the buggy function:
```python
if values_passed and not values_multi and not table.empty and (table.columns.nlevels > 1):
    table = table[values[0]]
```
Here, when `columns` is a multi-level index, the `table` object is erroneously considered as a `Series` object instead of a `DataFrame`.

### Bug Cause:
The bug is caused by incorrectly handling the conversion of `table` to a single column DataFrame when it is expected to have multiple columns due to multi-level columns in the input data.

### Fix Strategy:
1. Check the type of the `table` object before processing it.
2. If the `table` object is a `Series`, convert it to a `DataFrame` before attempting to access its `columns`.

### Fixed Version:
Here is the corrected version of the `pivot_table` function with the bug fixed:

```python
def pivot_table(...):
    # Existing code...

    if values_passed and not values_multi and not table.empty and (table.columns.nlevels > 1):
        if isinstance(table, ABCSeries):  # Check if table is a Series
            table = table.to_frame()  # Convert Series to DataFrame
        table = table[values[0]]  # Continue processing as DataFrame

    # Existing code...

    return table
```

By adding the check for `ABCDataFrame` class before accessing `columns` attribute, the bug related to handling multi-level columns should be resolved.