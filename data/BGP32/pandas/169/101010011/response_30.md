### Analysis:
1. The `quantile` function in the `DataFrame` class of `pandas.core.frame.py` is meant to perform quantile calculations on the DataFrame.
2. The error points to a concatenation issue while trying to compute quantiles, indicating an error related to the internal data manipulation.
3. The GitHub issue highlights that while `pd.Series(pd.date_range('1/1/18', periods=5)).quantile()` works fine, `pd.DataFrame(pd.date_range('1/1/18', periods=5)).quantile()` raises a `ValueError`. This suggests an issue specifically with datetime data in the quantile computation for DataFrames.
4. The error occurs when the DataFrame contains datetime data, and the `_get_numeric_data()` method could be causing the issue.
5. To fix the bug, we need to handle datetime data correctly in the quantile calculation.

### Bug Fix Strategy:
1. Identify the error in handling datetime data during quantile computation.
2. Adjust the approach to handle different types of data, such as datetime data, based on `numeric_only` parameter.
3. Ensure that the function can correctly determine whether to concatenate data arrays based on the passed parameters.
4. Make necessary adjustments to ensure the correct quantile computation for DateFrame.

### Corrected Version:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self if not numeric_only else self.select_dtypes(include=[np.number])
    axis = self._get_axis_number(axis)
    transposed = axis == 1

    if transposed:
        data = data.T

    result = data._data.quantile(qs=q, axis=1, interpolation=interpolation, transposed=transposed)

    if result.ndim == 2:
        result = self._constructor(result)
    else:
        result = self._constructor_sliced(result, name=q)

    if transposed:
        result = result.T

    return result
```

By using the `select_dtypes` method with `include=[np.number]`, we ensure that only numeric columns are selected for quantile computation. This way, we avoid the concatenation issue related to non-numeric data types like datetime in the DataFrame.