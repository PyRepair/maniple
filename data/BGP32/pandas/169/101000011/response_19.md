### Analysis:
- The buggy function `quantile` within the `DataFrame` class is supposed to return values at the given quantile over the requested axis but is causing an issue when dealing with datetime data.
- The GitHub issue "DataFrame Quantile Broken with Datetime Data" highlights that the `quantile` method is not working as expected with datetime data in a DataFrame, leading to a `ValueError: need at least one array to concatenate`.
- The issue seems to be related to the handling of datetime data within the `quantile` method.

### Identified Error Locations:
1. The `_get_numeric_data()` method may not handle datetime data appropriately.
2. The error is triggered during the concatenation process in the `_concat_compat` function when dealing with blocks that contain datetime data.

### Bug Cause:
- The bug arises due to the incorrect handling of datetime data within the `quantile` method. When datetime data is encountered, the method fails to concatenate the values properly, leading to a `ValueError`.

### Bug Fix Strategy:
- To resolve the bug, we need to ensure that if the data contains datetime values, it is handled correctly during the processing steps to avoid the concatenation issue.
- Modify the logic to handle datetime data in a way that is compatible with the concatenation process.

### Corrected Version of the function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)
    
    data = self.select_dtypes(include=[np.number]) if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1
    
    if is_transposed:
        data = data.T
    
    result = data._data.quantile(
        qs=q, axis=1, interpolation=interpolation, transposed=is_transposed
    )
    
    if result.ndim == 2:
        result = self._constructor(result)
    else:
        result = self._constructor_sliced(result, name=q)
    
    if is_transposed:
        result = result.T
    
    return result
```

By modifying the logic within the `quantile` function to correctly handle datetime data by using `select_dtypes()` to filter only numeric columns, we can avoid the `ValueError` when dealing with datetime values. This corrected version should address the issue reported in the GitHub bug.