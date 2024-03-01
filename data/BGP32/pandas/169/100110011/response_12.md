### Analysis:
1. The buggy function is `quantile()` in the `pandas/core/frame.py` file.
2. The failing test is `test_quantile_empty_no_columns` in `pandas/tests/frame/test_quantile.py`.
3. The error message indicates a `ValueError` due to needing at least one array to concatenate.
4. The cause of the bug seems to be related to how the DataFrame is created with date-time values and then processed by the `quantile()` function.
5. To fix the bug, we need to handle date-time values correctly within the function.

### Bug Cause:
The bug causes a `ValueError` because when creating a DataFrame with date-time values, the function does not handle them properly, leading to the concatenation error.

### Bug Fix Strategy:
To fix the bug, we need to modify the `_get_numeric_data` process to ensure that relevant data is fetched correctly, especially when date-time columns are present.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)
    
    if not numeric_only:
        data = self
    elif len(self._get_numeric_data()._info_axis) == 0:
        data = self.copy()
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

By modifying the logic for fetching numeric data, the function now correctly handles date-time columns, preventing the concatenation error and resolving the bug.