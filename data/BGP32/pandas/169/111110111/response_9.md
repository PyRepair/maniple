To fix the bug in the `quantile` function of the `DataFrame` class, we need to ensure that when the input DataFrame contains datetime data and no numeric data, the function handles this case correctly without attempting to concatenate empty arrays.

The issue arises when the input DataFrames do not contain any numeric values, leading to an error during concatenation. To address this problem, we can modify the function to handle the scenario where all columns are dropped during the quantile computation.

Here is a corrected version of the `quantile` function:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)
    
    data = self._get_numeric_data() if numeric_only else self
    if len(data.columns) == 0:
        return self._constructor_sliced([], index=[q], columns=[])
    
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

This corrected version includes a check for empty columns in the data after extracting numeric data. If all columns are dropped, it directly constructs the appropriate output DataFrame with empty values.

With this correction, the function should now handle cases where all columns are dropped during quantile computation, preventing the concatenation error and returning the expected output for the failing test case you provided.