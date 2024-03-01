### Bug Analysis:
1. The buggy function `quantile()` in the `pandas.core.frame.DataFrame` class, is designed to return values at the given quantile over a specified axis for the DataFrame object.
2. The error message points to a concatenation issue inside the function, specifically relating to the empty nature of the DataFrame passed as input.
3. The function is failing for inputs containing datetime data because the function fails to handle the datetime data properly, causing the internal calculation to produce an empty result leading to the concatenation error.
4. To fix the bug, a check needs to be implemented to handle empty DataFrames correctly when dealing with datetime data.

### Bug Fix Strategy:
To fix the bug, the correction involves adding a check to handle the scenario where the DataFrame contains datetime data and is empty during quantile calculation. This check should prevent the function from attempting to concatenate empty arrays.

### Corrected Code:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self
    
    # Check if datetime data columns exist and they're all null to avoid the concatenation issue
    if not data.select_dtypes(include='datetime64').notnull().any().any():
        return data

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

By implementing the correction described above, the `quantile()` function should now handle empty DataFrames containing datetime data without raising a `ValueError: need at least one array to concatenate`.