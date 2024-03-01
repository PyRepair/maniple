### Bug Analysis
The bug occurs when the input DataFrame does not contain any numeric data columns. In this case, the `_get_numeric_data` method in the buggy function returns an empty DataFrame, leading to an error when trying to compute the quantile. This situation causes the concatenation function to fail due to needing at least one array to concatenate, as indicated by the error message.

### Bug Fix Strategy
To fix this bug, we need to handle the case when the input DataFrame does not have any numeric data columns. We can modify the code to check for this scenario and return an appropriate result, such as NaN or an empty DataFrame. 

We also need to ensure that the quantile computation can handle empty DataFrames or adjust the workflow accordingly.

### Corrected Function
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    if self.empty:
        # Return an empty result since the input DataFrame is empty
        return self._constructor_empty()

    data = self._get_numeric_data() if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    if data.empty:
        # Return an empty result since there are no numeric columns
        return self._constructor_empty()

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

### Explanation
1. The corrected function first checks if the input DataFrame `self` is empty. If it is empty, the function returns an empty result using the `_constructor_empty` method.

2. Next, it checks if there are any numeric columns in the DataFrame. If there are no numeric columns, the function returns an empty result as well.

3. If there are numeric columns, the quantile computation proceeds as before.

By implementing these checks, the corrected function handles the scenario where the input DataFrame does not have any numeric data columns, preventing the concatenation error.