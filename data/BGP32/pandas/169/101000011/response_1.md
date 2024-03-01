## Analysis:
1. The `quantile` method in the `DataFrame` class is supposed to calculate the quantiles of the data along the specified axis. 
2. The related function `_get_numeric_data()` is used to filter out only the numeric data when `numeric_only` is set to `True` to ensure proper quantile calculation.
3. The issue reported on GitHub highlights a case where using `pd.DataFrame(pd.date_range('1/1/18', periods=5)).quantile()` raises a `ValueError` when attempting to calculate the quantiles of datetime data. It seems that the bug is related to handling non-numeric data types like datetime.
4. In the current implementation, when the data coming into the `quantile` function is non-numeric, it still tries to perform the quantile calculations which lead to the error. The system should handle this scenario correctly.
5. To fix this bug, we need to modify the quantile function to check the data type before attempting quantile calculations and handle non-numeric data appropriately.

## Suggested Fix:
1. We will modify the `quantile` function to filter out non-numeric data correctly when `numeric_only` is set to `True`.
2. We will check the data type of the input data and only perform quantile calculations on the numeric data.
3. This will ensure that the function does not attempt to concatenate non-numeric data and avoid the `ValueError` raised in the issue.

## Corrected Version:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    # Filter out non-numeric data if numeric_only is True
    data = self._get_numeric_data() if numeric_only and self._data.get_dtype_counts().get("datetime64") == 0 else self

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

With this corrected version, the `quantile` function will now correctly handle the case where non-numeric data, such as datetime data, is passed to the function. This change should resolve the issue reported on GitHub and ensure that quantile calculations are performed only on numeric data, avoiding the `ValueError` encountered previously.