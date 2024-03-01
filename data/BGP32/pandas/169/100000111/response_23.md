### Bug Analysis
The bug arises when the `quantile` function is applied to a DataFrame containing datetime data. The function attempts to concatenate values without considering datetime data, leading to the "ValueError: need at least one array to concatenate" error.

### Bug Fix Strategy
To fix the bug, the function needs to handle datetime data properly when computing quantiles for a DataFrame. Specifically, it should separate the treatment of datetime data versus other numeric data.

### Corrected Function
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    if numeric_only:
        data = self._get_numeric_data()
    else:
        data = self.select_dtypes(include=[np.number, 'datetime'])
    
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    result = data._data.quantile(
        qs=q, axis=1, interpolation=interpolation, transposed=is_transposed
    )

    result = self._constructor(result)
    
    if is_transposed:
        result = result.T

    return result
```

### Explanation
The corrected function includes a conditional selection of data based on whether `numeric_only` is `True`. If `numeric_only` is `False`, the function selects columns that are of type `np.number` or 'datetime'. This ensures that the function can handle datetime data appropriately without trying to concatenate incompatible data types.

The corrected function should now successfully calculate quantiles for DataFrame containing datetime data and return the correct output as expected.