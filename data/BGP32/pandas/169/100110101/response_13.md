### Bug Analysis:
The bug is caused by the `concat_compat` function trying to concatenate empty arrays, which leads to a `ValueError` since there are no arrays to concatenate. This occurs when the `_get_numeric_data()` method returns an empty DataFrame due to the absence of numeric data in the input DataFrame.

### Bug Fix Strategy:
We need to handle the case where `_get_numeric_data()` returns an empty DataFrame by checking for empty data before proceeding to calculate the quantile. If the data is empty, we should return an empty Series or DataFrame accordingly.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self

    if data.empty:
        if isinstance(q, (float, int)):
            return pd.Series()
        else:
            return pd.DataFrame()
    
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

By adding a check for an empty DataFrame before calculating the quantile, we can avoid the `ValueError` when trying to concatenate empty arrays, ensuring the function works correctly in cases where the input data is empty.