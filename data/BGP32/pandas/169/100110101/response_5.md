### Error Analysis:
- The error message indicates a `ValueError: need at least one array to concatenate` in the `quantile` function.
- The test case involves an empty DataFrame `df` created using `pd.DataFrame(pd.date_range("1/1/18", periods=5))`, where all columns are of type `datetime64[ns]`, leading to no numeric data for quantile calculation.
- The function tries to concatenate values during the quantile computation, which fails due to no numeric data available.
- The `self._get_numeric_data()` method is supposed to filter out non-numeric data, but since all columns are datetime objects, it results in an empty DataFrame.

### Bug Fix Strategy:
- The bug fix involves enhancing the logic to handle cases where there is no numeric data available for quantile calculation. 
- We need to add a check to handle scenarios where all columns are non-numeric, such as datetime objects.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only and self._get_numeric_data().shape[1] > 0 else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    if data.empty:
        result = self._constructor()
    else:
        result = data._data.quantile(qs=q, axis=1, interpolation=interpolation, transposed=is_transposed)

        if result.ndim == 2:
            result = self._constructor(result)
        else:
            result = self._constructor_sliced(result, name=q)

    if is_transposed:
        result = result.T

    return result
```

By adding a condition to check if the numeric data exists in the DataFrame before proceeding with quantile calculation, the function will no longer throw errors when dealing with datasets containing only non-numeric data, such as datetimes.