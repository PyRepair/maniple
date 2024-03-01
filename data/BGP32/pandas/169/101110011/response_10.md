### Explanation of the Bug:

The bug occurs in the `DataFrame` class's `quantile` method when it is called with datetime data. The `_check_percentile(q)` call attempts to validate the input `q`, but then it directly uses the function `self._get_numeric_data()` which only retrieves numeric data, thereby omitting non-numeric datetime data.

When the `DataFrame` contains only datetime columns, `_get_numeric_data()` effectively returns an empty DataFrame resulting in an empty Series. Subsequently, the code attempts to concatenate these empty results which leads to the `ValueError: need at least one array to concatenate`.

### Fixing the Bug:

To fix the bug, we need to ensure that when `numeric_only` is set to `False`, the method includes both numeric and non-numeric data. We can modify the logic to check if any non-numeric data exists before deciding to use `_get_numeric_data()`.

### Corrected Version:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)
    
    if not numeric_only:
        data = self
    else:
        data = self._get_numeric_data()
    
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

This corrected version improves the method's logic by considering all data when `numeric_only` is set to `False`, thus avoiding the issue with empty results and concatenation. This change should resolve the bug and allow the failing test to pass as expected.