### Analysis:
- The `ValueError: need at least one array to concatenate` error message suggests that the `concat_compat` function is trying to concatenate empty arrays, which is not allowed and hence causing an error.
- The error is occurring in the `quantile()` function, specifically in the line `result = data._data.quantile(qs=q, axis=1, interpolation=interpolation, transposed=is_transposed)`.
- The issue arises when `data._data` is empty, leading to the attempt to concatenate empty arrays.

### Bug Cause:
The `_get_numeric_data()` function may return an empty DataFrame when `numeric_only` is set to `True`, which in turn results in an attempt to concatenate empty arrays in the `quantile()` function.

### Bug Fix:
- To fix this bug, we need to add a check for an empty DataFrame before calling the `_data.quantile()` function.
- If the `data` DataFrame is empty, we should return an empty DataFrame or Series based on the type of quantile values provided.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self

    if len(data) == 0:
        if isinstance(q, (list, tuple, np.ndarray)):
            result = pd.DataFrame(columns=self.columns, index=q)
        else:
            result = pd.Series(index=self.columns)
        return result

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

### Summary:
- The corrected function now includes a check for an empty DataFrame `data` and returns an appropriately structured DataFrame or Series based on the input quantile values.
- This fix ensures that the function does not attempt to concatenate empty arrays, resolving the `ValueError` and correcting the behavior of the `quantile()` function.