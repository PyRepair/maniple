### Analysis:
The buggy function `quantile` in the `pandas.core.frame` module is supposed to return values at the given quantile over the requested axis, handling numeric and datetime data with the specified interpolation method. The reported issue on GitHub highlighted a problem where the `DataFrame.quantile()` method raises a `ValueError` when working with datetime data, while the `Series.quantile()` method functions correctly.

### Error Locations:
1. The `_get_numeric_data()` method may not handle datetime data properly.
2. The construction of `result` using `data._data.quantile()` may not work as expected for datetime data.

### Bug Cause:
The bug occurs because the function does not handle the case of datetime data appropriately. When working with datetime data, the function tries to concatenate the internal data blocks of the frame, causing a `ValueError` because datetime data blocks cannot be concatenated directly.

### Strategy for Fixing the Bug:
1. Implement a check to handle datetime data specifically.
2. Modify data handling when computing the quantile.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    if isinstance(data, pd.DataFrame) and data.select_dtypes(include=['datetime64', 'timedelta64']).size > 0:
        result = data.select_dtypes(include=['datetime64', 'timedelta64']).quantile(q=q, axis=1, interpolation=interpolation)
    else:
        result = data._data.quantile(qs=q, axis=1, interpolation=interpolation, transposed=is_transposed)

    if result.ndim == 2:
        result = self._constructor(result)
    else:
        result = self._constructor_sliced(result, name=q)

    if is_transposed:
        result = result.T

    return result
```

### Correction Rationale:
- Added a check to handle datetime data specifically by selecting only datetime columns for quantile computation.
- Used different quantile computation strategy for datetime data to avoid concatenation issues.

By implementing this corrected function, the issue reported on GitHub where `DataFrame.quantile()` raises a `ValueError` with datetime data should be resolved.