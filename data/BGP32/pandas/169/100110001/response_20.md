### Analysis:
1. The error message is indicating a `ValueError` with the message "need at least one array to concatenate" when trying to concatenate arrays in the `concat_compat` function.
2. The `quantile` function in the source code extracts numeric data based on the `numeric_only` parameter to compute quantiles. In the failing test, the DataFrame `df` has all columns containing dates, which are not considered numeric data.
3. The `quantile` function is trying to extract numeric data using `_get_numeric_data()` method, but when all columns are non-numeric, it results in an empty DataFrame which causes the concatenation error later on.
4. To fix the bug, we need to handle the case where all columns are non-numeric in the DataFrame by returning appropriate empty Series or DataFrame based on the input `q` in the function.
  
### Solution:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if data.empty:
        if isinstance(q, list):
            result = self._constructor([], columns=self.columns, index=q)
        else:
            result = self._constructor([], index=self.columns)
        return result

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

By checking if the DataFrame is empty after extracting numeric data, we can appropriately handle the case where all columns are non-numeric, preventing the concatenation error in such scenarios.