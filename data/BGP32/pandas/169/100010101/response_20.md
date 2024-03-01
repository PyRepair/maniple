### Bug Explanation
The bug occurs because the `_get_numeric_data()` method returns an empty DataFrame when applied to a DataFrame composed solely of datetime values. This results in an empty data frame being passed to the `quantile()` method, leading to an error when attempting to compute the quantile. 

The error message `ValueError: need at least one array to concatenate` is triggered because the function is trying to concatenate empty arrays, which is not allowed.

### Bug Fix Strategy
To fix this bug, we need to handle the case where `_get_numeric_data()` returns an empty DataFrame by adding a conditional check before computing the quantile. If the DataFrame is empty after applying `_get_numeric_data()`, we should return an empty DataFrame or Series, depending on the type of input `q`.

### Corrected Version
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data()
    if data.empty:
        # Handle case where data is empty
        if isinstance(q, (list, np.ndarray)):
            return self._constructor_sliced(np.nan, index=q)
        else:
            return self._constructor_sliced(np.nan, name=q)

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

This corrected version handles the case where the data returned from `_get_numeric_data()` is empty by returning an empty DataFrame or Series.