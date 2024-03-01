### Bug Explanation
The bug in the `quantile` function arises from the scenario where `data` becomes an empty DataFrame after applying the `numeric_only` condition. In this case, `data._data` still tries to quantile over no data, leading to the error `ValueError: need at least one array to concatenate`.

### Bug Fixing Strategy
To fix the bug, we need to handle the case where `data` becomes empty by checking if the `data` DataFrame is empty. If it is empty, we should return an empty Series or DataFrame depending on the input `q` parameter.

### Corrected Function

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    """
    Return values at the given quantile over requested axis.
    
    """
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T
        
    if data.empty:  # Handle the case where data is empty
        if isinstance(q, list):
            return self._constructor(data)
        else:
            return self._constructor_sliced(data, name=q)

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

The corrected function checks if the `data` DataFrame is empty and returns an empty Series or DataFrame based on the type of `q` parameter. This ensures that the function can handle the scenario where `data` is empty and prevents the `ValueError` that was occurring before.