### Bug Analysis:
The error message "ValueError: need at least one array to concatenate" is occurring at the `concat_compat` function due to an empty list being passed for concatenation. This happens because the `data._data` attribute results in an empty `BlockManager` object when `numeric_only` is set to `True` and no numeric columns are present. This causes issues during the quantile calculation.

### Bug Fix Strategy:
To fix this bug, we need to adjust the logic for handling empty data frames in the `quantile` function. We should check if there are numeric columns available before proceeding with the quantile calculation. If no numeric data is present, the function should return an appropriate message or empty results.

### Corrected Code:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    
    self._check_percentile(q)
    
    if numeric_only and len(self.select_dtypes(include=['number']).columns) == 0:
        # No numeric columns present to compute quantiles.
        return pd.DataFrame(columns=self.columns, index=[0.5], data='No numeric data to compute quantile')
    
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

By adding the check for numeric columns before proceeding with the quantile calculation, we ensure that the function handles empty data frames appropriately and avoids concatenation errors. This corrected version should pass the failing test cases and provide the expected output.