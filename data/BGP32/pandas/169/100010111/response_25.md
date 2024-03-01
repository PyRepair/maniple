### Analysis:
1. The `quantile` function in the `DataFrame` class is supposed to compute quantiles over requested axis for the provided data frame.
2. The error is triggered due to empty data blocks causing the concatenation function to fail with "ValueError: need at least one array to concatenate".
3. The function fails to handle the case where there are no numeric columns (empty data), leading to the issue.
4. To fix this bug, the function should handle the case of empty data gracefully and return an appropriate output.

### Bug Explanation:
In the failing test with an empty DataFrame of non-numeric data, the current implementation fails to handle the case where there are no columns to compute quantiles. The error message shows that there's an issue with concatenation due to empty arrays, indicating that the function is trying to concatenate empty data arrays, causing the ValueError.

### Bug Fix Strategy:
1. Check if there is any numeric data available before trying to compute quantiles.
2. If there is no numeric data, return an empty Series or DataFrame based on the input `q`.
3. Update the implementation to handle the case of empty data in a way that prevents the concatenation of empty arrays.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data()
    if data.empty:
        if isinstance(q, list):
            result = pd.DataFrame(index=q, columns=self.columns)
        else:
            result = pd.Series()
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

The corrected `quantile` function now correctly handles the case of empty data in the DataFrame and returns an appropriate output without triggering the ValueError related to concatenation of empty arrays.