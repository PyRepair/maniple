The bug in the provided function is due to the incorrect extraction of numeric data in the `quantile` function. The function `self._get_numeric_data()` is being called assuming it will retrieve numeric data from the DataFrame, but in the case of a DataFrame with datetime data, the function does not handle it correctly. This leads to an error when trying to compute quantiles on non-numeric data.

To fix the bug, we need to modify the extraction of data depending on whether `numeric_only` is set to `True` or `False`. If `numeric_only` is `False`, we should consider all data types for computing quantiles, including datetime data.

Here is the corrected and updated version of the `quantile` function:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)
    
    if not numeric_only:
        data = self
    else:
        data = self._get_numeric_data()
        
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

This corrected version of the function checks the `numeric_only` parameter correctly and uses all data if `False`. This change ensures that the function does not throw an error when dealing with non-numeric data like datetime values as mentioned in the GitHub issue description.

This fix should resolve the issue reported in the GitHub bug concerning DataFrame quantiles not working with datetime data.