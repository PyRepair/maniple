### Bug Analysis:
The bug occurs when the function tries to concatenate empty arrays which results in a `ValueError`. The issue arises from the `_get_numeric_data()` method call within the function, which is returning an empty DataFrame when no numeric columns are present.

### Bug Fix Strategy:
We need to handle the case where `_get_numeric_data()` returns an empty DataFrame to avoid the concatenation error. This can be achieved by checking if the `data` DataFrame is empty before proceeding with the quantile calculation.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data()
    if data.empty:
        return self._constructor_empty(data, index=q) 
    
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

This corrected version of the function checks if the `data` DataFrame is empty after calling `_get_numeric_data()`. If the DataFrame is empty, it directly returns an empty DataFrame based on the input `q`. This prevents the concatenation error and ensures proper handling of the edge case.