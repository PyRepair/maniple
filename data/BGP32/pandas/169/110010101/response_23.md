### Analysis:
1. The `quantile` function in the `DataFrame` class is designed to return values at the given quantile over the requested axis.
2. The error message shows a `ValueError` indicating that there is a need for at least one array to concatenate. This suggests that the function is trying to concatenate empty arrays, leading to the error.
3. The input DataFrame has one column with dates, and when trying to compute quantiles on this, it results in an empty DataFrame which causes the function to fail.
4. To fix this, we need to handle the case where there are no numeric columns in the DataFrame, and skip the quantile calculation in such cases. We should return an empty DataFrame or Series as appropriate.

### Fix Strategy:
1. Check if the DataFrame contains any numeric columns using the `_get_numeric_data` method.
2. If there are no numeric columns, return an empty DataFrame or Series based on the input parameter `q`.
3. Update the return statements to handle the case where no data is available.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self
    
    if data.empty:
        if isinstance(q, (float, int)):
            return pd.Series(index=self.columns, data=[np.nan]*len(self.columns), name=q)
        else:
            return pd.DataFrame(index=q, columns=self.columns, data=[[np.nan]*len(self.columns) for _ in range(len(q))])

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

The corrected function now checks for empty data frames and returns the required structure with NaN values when no numeric data is present. Now the function should handle cases where there are no numeric columns in the input DataFrame.