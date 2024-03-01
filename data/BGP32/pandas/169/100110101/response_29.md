### Bug Analysis:
The error message "ValueError: need at least one array to concatenate" suggests an issue with concatenation when attempting to compute quantiles. The function first filters the data based on the `numeric_only` parameter and transposes it if the `axis` is set to 1 (columns). The problem likely arises during the quantile calculation step.

### Bug Explanation:
1. The function `_get_numeric_data()` filters the dataframe based on the `numeric_only` parameter, but in the failing test, the provided dataframe `df` contains only datetime values. As a result, after filtering, the dataframe becomes empty, leading to the concatenation error.
2. The error originates when attempting to concatenate empty arrays with `np.concatenate` inside the `_data.quantile` method.

### Bug Fix Strategy:
To fix the bug, we need to handle the case where the filtered data becomes empty correctly. If the filtered data is empty due to the `numeric_only` filtering, the function should return an appropriate empty `Series` or `DataFrame` based on the input `q`.

### Corrected Function:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    if data.empty:  # Handle case where filtered data is empty
        if isinstance(q, list):
            result = self._constructor(index=q, data=None)
        else:
            result = self._constructor_sliced(data=None, name=q)
    else:
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

By including an explicit check for empty data and handling it appropriately to return the expected empty `Series` or `DataFrame`, the corrected function should now pass the failing test cases and meet the expected input/output values.