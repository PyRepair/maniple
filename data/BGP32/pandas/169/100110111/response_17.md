### Analysis:
1. The buggy function, `quantile`, is supposed to return values at the given quantile over the requested axis based on the input parameters.
2. The failing test case, `test_quantile_empty_no_columns`, initializes a DataFrame `df` containing date-range data and attempts to retrieve the 0.5 quantile, which triggers an error during the function execution.
3. The error occurs in the `quantile` function at the line `result = data._data.quantile(qs=q, axis=1, interpolation=interpolation, transposed=is_transposed)`, specifically within the `quantile` method of `_data` property due to a concatenation issue.
4. The bug arises as `_data` contains no blocks to concatenate, leading to the `ValueError: need at least one array to concatenate`.
5. To fix this bug, we need to ensure that the operation correctly handles cases where there are no blocks to concatenate and adjust the handling of data and its transposition.

### Bug Fix Strategy:
To fix the bug, we can address the root cause by implementing a check for empty data conditions and adjust the internal block concatenation logic to handle these scenarios gracefully.

### Bug-Fixed Version:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    if not data.empty:
        result = data._data.quantile(
            qs=q, axis=1, interpolation=interpolation, transposed=is_transposed
        )
        
        if result.ndim == 2:
            result = self._constructor(result)
        else:
            result = self._constructor_sliced(result, name=q)

        if is_transposed:
            result = result.T
    else:
        if isinstance(q, list):
            result = pd.DataFrame([], index=q, columns=[])
        else:
            result = pd.Series([], index=[], name=q)

    return result
```

By implementing the bug-fix changes highlighted above, the `quantile` function should now handle the empty data condition and avoid the concatenation issue that led to the initial error. Running the failing test case again should now pass without raising the `ValueError`.