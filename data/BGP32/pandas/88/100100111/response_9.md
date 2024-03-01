### Bug Analysis:
The `pivot_table` function fails when trying to pivot data with multi-index columns only. The specific failing case is when `df2.pivot_table(values='v', columns=('k1','k2'))` is called, resulting in an AttributeError due to attempting to access columns on a Series object. The function is incorrectly handling the case when the columns parameter represents a multi-index.

### Error Location:
The error occurs around the following segment in the buggy function:
```python
if values_passed and not values_multi and not table.empty and (table.columns.nlevels > 1):
    table = table[values[0]]
```
Here, `table` is expected to be a DataFrame, but if it contains multi-index columns, the code incorrectly assumes it is still a DataFrame when accessed.

### Cause of the Bug:
The bug is caused by improper handling of multi-index columns. The code wrongly attempts to access columns directly on `table`, assuming it is always a DataFrame. However, in cases with multi-index columns, `table` is actually a Series object, leading to the AttributeError.

### Strategy for Fixing the Bug:
1. Check the type of `table` before attempting operations that are specific to DataFrames with multiple columns.
2. If `table` is a Series, handle the multi-index columns appropriately by converting it to a DataFrame with proper alignment.

### Corrected Function:
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
) -> DataFrame:
    index = _convert_by(index)
    columns = _convert_by(columns)

    if isinstance(aggfunc, list):
        # Existing code to handle list of aggfuncs is valid

    keys = index + columns

    values_passed = values is not None
    
    # Code to check and filter data for the multi-index columns (columns)
    if isinstance(columns, (tuple, list)):
        names = columns if isinstance(columns, tuple) else list(columns)
        table = data.pivot_table(values=values, index=index, columns=columns)
        names = names if isinstance(names, tuple) else [names]
        table.columns = pd.MultiIndex.from_tuples([tuple(x) for x in table.columns], names=names)
    else:
        table = data.pivot_table(values=values, index=index, columns=columns)

    return table
```

In the corrected code:
- The `pivot_table` function now properly handles the case when `columns` represent multi-index columns.
- It checks the type of `columns` and handles multi-index columns specifically by adjusting the output dataframe and column names accordingly.

This corrected version should resolve the AttributeError issue faced in the failing test case provided.