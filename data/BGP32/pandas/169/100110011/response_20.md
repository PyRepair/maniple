### Bug Analysis:
1. The buggy function `quantile` in `pandas/core/frame.py` is designed to compute the quantiles of a DataFrame, but it fails when the DataFrame contains datetime data.
2. The failing test `test_quantile_empty_no_columns` in `pandas/tests/frame/test_quantile.py` demonstrates the error when calling `df.quantile(0.5)` on a DataFrame with datetime values.

### Error Cause:
1. The main cause of the bug is that the `quantile` function tries to concatenate arrays of datetime values, leading to a `ValueError: need at least one array to concatenate`.
2. This error occurs because datetime values cannot be concatenated directly like numerical values.

### Bug Fix Strategy:
To fix the bug, we need to:
1. Modify the `quantile` function to handle datetime values appropriately.
2. Ensure that the function properly handles the internal representation of datetime values.

### Corrected Version of the `quantile` function:
Here is the corrected version of the `quantile` function:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)
    data = self._get_numeric_data() if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    if not data.empty and (data.dtypes != 'datetime64[ns]').all():
        result = data._data.quantile(
            qs=q, axis=1, interpolation=interpolation, transposed=is_transposed
        )
    else:
        result = data.quantile(q=q, axis=1, numeric_only=numeric_only, interpolation=interpolation)

    if result.ndim == 2:
        result = self._constructor(result)
    else:
        result = self._constructor_sliced(result, name=q)

    if is_transposed:
        result = result.T

    return result
```

### Explanation of Changes:
1. The corrected version of the function checks if the DataFrame contains only datetime data (no numerical data to quantify), if so, it properly hands over the calculation to the `quantile` function of the `Series`, which is able to handle datetime values.
2. By providing proper handling for datetime values, the function now computes quantiles correctly for DataFrames as well.

By incorporating these changes, the function should now correctly handle quantiles for DataFrames with datetime data without raising a `ValueError`.