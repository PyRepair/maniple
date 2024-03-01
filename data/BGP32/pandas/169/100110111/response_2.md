### Error Analysis:
1. The function `quantile` first ensures that the input `q` is within bounds by calling `_check_percentile(q)`.
2. It then chooses to use numeric data only if `numeric_only` is True. Otherwise, it uses the whole dataframe.
3. The axis is set based on whether the requested processing should be done row-wise or column-wise.
4. Depending on the axis, the data is transposed to facilitate processing.
5. The quantiles are calculated with the specified interpolation method, and the result is transformed back if needed.

### Bug Cause: 
The error occurs because when the data processing skips all numeric columns due to the condition `numeric_only`, there is nothing to concatenate later. In the failing test, the DataFrame created from `pd.date_range('1/1/18', periods=5)` has no numeric data. When `quantile` is called, the function fails because there are no arrays to concatenate.
The bug violates the expected functionality stated in the GitHub issue. The function should indeed return a Series when the input DataFrame is without numeric data.

### Bug Fix Strategy:
To fix the bug, we need to modify the function to handle scenarios where there are no numeric columns present in the DataFrame. This would involve checking if the data to be processed after filtering out non-numeric columns is empty, and then dealing with this scenario correctly.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if not len(data.columns):
        result = pd.Series([], index=[], name=q) if isinstance(q, float) else pd.DataFrame([], index=q, columns=[], name=q)
    else:
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

Now, the corrected function will correctly check for the presence of numeric columns before proceeding with the quantile calculation. If no numeric columns are found, it will return an empty Series or DataFrame as per the expectations. This fix addresses the bug that caused the function to fail when handling DataFrame instances without numeric data.