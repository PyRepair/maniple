The bug in the `quantile` function arises from the use of `self._get_numeric_data()` to filter the DataFrame based on the `numeric_only` parameter. If all columns are non-numeric, then `self._get_numeric_data()` will return an empty DataFrame, leading to incorrect behavior in the `quantile` function.

To fix the bug, we need to handle the case where `data` is empty after filtering based on `numeric_only`. In this case, we should return an empty DataFrame or Series based on the shape of the input DataFrame.

Here is the corrected version of the `quantile` function:

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

    if data.empty:
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

With this correction, the `quantile` function should handle the case when `data` is empty correctly and return an empty DataFrame or Series as expected. This should resolve the failing test case provided above.