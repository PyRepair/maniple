### Potential Error Locations
1. The error seems to occur during concatenation in the `quantile` function, specifically in the line `values = concat_compat([b.values for b in blocks])`.
2. This indicates that there might be an issue in obtaining the values from the individual blocks in the data, leading to an empty list that cannot be concatenated.

### Bug Cause Analysis
1. The issue arises when `pd.DataFrame(pd.date_range('1/1/18', periods=5)).quantile()` is called where only date data is provided to a DataFrame instead of numeric data.
2. The `quantile` function expects numeric data to compute the quantile values, but since it's the only datetime data, an attempt to concatenate empty arrays leads to a `ValueError`.

### Bug Fixing Strategy
To fix this bug, we need to modify the `quantile` function to handle datetime data appropriately. When data is not numeric, it should directly return the data without trying to proceed with quantile calculations.

### Corrected Version of the `quantile` Function
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    if not any(self._get_numeric_data()):
        # No numeric data available, return the original data
        return self

    data = self._get_numeric_data() if numeric_only else self
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

With this modification, the `quantile` function will first check if any numeric data is present. If not, it will return the original data without attempting further calculations, avoiding the `ValueError` during concatenation.