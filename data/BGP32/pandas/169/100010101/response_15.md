### Bug Explanation:
The bug occurs because the function is trying to concatenate empty arrays when the `data` DataFrame doesn't contain any numeric data after filtering with `numeric_only`. This leads to an error when trying to calculate the quantile.

### Bug Fix Strategy:
To fix the bug, we need to adjust the logic in the function to handle the case where no numeric data is present after filtering. Instead of directly calculating the quantile, we should return an appropriate empty DataFrame or Series based on the input parameter `q`.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self

    if data.empty:
        return self._constructor() if isinstance(q, float) else self._constructor_sliced()

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

This corrected version of the function checks if the `data` DataFrame is empty before attempting to calculate the quantile. In case the DataFrame is empty, it immediately returns an appropriate empty DataFrame or Series based on the input parameter `q`. This prevents the concatenation error from occurring in the original buggy function.