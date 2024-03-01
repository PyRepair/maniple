### Issues:
1. The function `quantile` in the `DataFrame` class has a bug that causes it to raise a `ValueError: need at least one array to concatenate` when called with datetime data.
2. The `_get_numeric_data()` function internal to the `quantile` function drops all columns resulting in an empty DataFrame, leading to the concatenation error.

### Bug Cause:
The root cause of the bug is the logic in `_get_numeric_data()` that drops all columns when the DataFrame contains datetime data. This leads to an empty DataFrame with no data to quantile, resulting in a concatenation error.

### Strategy to Fix the Bug:
1. Check for the presence of numeric data before dropping columns in the `_get_numeric_data()` function.
2. Refactor the logic to handle datetime data separately to avoid dropping all columns.

### Corrected Version of the Function:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation='linear'):
    """
    Return values at the given quantile over requested axis.
    """
    self._check_percentile(q)

    data = self.select_dtypes(include=[np.number]) if numeric_only else self
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

This corrected version checks for numeric data using `select_dtypes` with `include=[np.number]` instead of dropping all columns. This change ensures that quantile can be calculated correctly without causing a concatenation error.