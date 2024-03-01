### Bug Explanation
The bug is caused by the function trying to concatenate empty arrays. In the failing test case, the DataFrame `df` contains only datetime values without any numeric data. When the `df.quantile(0.5)` or `df.quantile([0.5])` is called, it goes through the function, attempts to extract numeric data using `_get_numeric_data()`, but since there is no numeric data available, it results in an empty DataFrame. Subsequently, during the quantile calculation in the function, it tries to concatenate these empty arrays, leading to the `ValueError: need at least one array to concatenate` error.

### Fix Strategy
To fix this bug, we need to handle the scenario where the DataFrame has no numeric data. Instead of trying to calculate quantiles on an empty dataset, we should return an empty `Series` or `DataFrame` depending on the input `q`.

### Corrected Function
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only and not self.empty else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    if self.empty:
        # Return an empty Series or DataFrame based on input q
        if isinstance(q, (list, tuple)):
            result = pd.DataFrame(index=q, columns=data.columns)
            result.columns.name = self.columns.name
        else:
            result = pd.Series(name=q, dtype=float)
            result.index.name = self.columns.name
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

By including a check for an empty DataFrame and handling it appropriately by returning either an empty Series or DataFrame based on the input `q`, the corrected function should now pass the failing test cases and satisfy the expected input/output values.