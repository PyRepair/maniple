### Explanation:
The bug in the `quantile` method arises when the input DataFrame `self` contains only datetime data, leading to an empty DataFrame after data processing. This causes issues with concatenation and fails to return the expected output.

The bug is related to how the method processes the input DataFrame when it contains datetime data. The `self._get_numeric_data()` call doesn't return any columns in this situation due to the absence of numeric data. Consequently, the following processing and construction steps lead to unexpected results.

### Error Location:
The bug exists in the `quantile` method when handling cases where the DataFrame contains only datetime data, resulting in an empty DataFrame, causing the concatenation failure and incorrect output.

### Bug Fix Strategy:
A suitable fix for the bug would involve modifying the data processing logic to consider cases where the DataFrame doesn't contain any numeric data. By detecting this scenario and adapting the construction of the result appropriately, we can ensure that the method works correctly for all types of input DataFrames.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)
    
    data = self._get_numeric_data() if numeric_only and len(self.select_dtypes(include=[np.number]).columns)>0 else self
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
        # Handle empty DataFrame with datetime data case
        if len(result.columns) == 0:
            result = self._constructor([], index=q, columns=self.columns)
            result.index.name = self.columns.name
        else:
            result = self._constructor_sliced(result, name=q)
    
    if is_transposed:
        result = result.T
    
    return result
```

By adding the check for the presence of numeric columns in the DataFrame and adjusting the result construction logic for the case of an empty DataFrame with datetime data, we ensure that the method handles the datetime data appropriately and returns the expected output for all scenarios.