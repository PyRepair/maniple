### Error Location:
The error occurs in the quantile function inside the DataFrame class, specifically in the `quantile` method of the `DataFrame` class in the `pandas/core/frame.py` file.

### Bug Cause:
The issue arises when the DataFrame has no numeric columns, and the `_get_numeric_data()` method returns an empty DataFrame. This empty DataFrame leads to an empty result in the quantile calculation which causes the error during concatenation.

When trying to compute the quantiles on a DataFrame that consists of non-numeric columns (e.g., datetime data), the privided quantile method calculates quantiles based on the provided axis and interpolation method, but it fails to handle the case when no numeric data is present.

### Bug Fix Strategy:
To address this issue, we need to modify the code so that it can handle the scenario when the DataFrame has no numeric columns. The quantile method should detect this case and return an appropriate empty output without trying to calculate quantiles. This can be achieved by checking if there is numeric data available before proceeding with the quantile calculation.

### Corrected Code:
Here is the corrected version of the `quantile` method that includes the necessary fix to handle the case when the DataFrame has no numeric columns:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    # Check if there are numeric columns
    if numeric_only:
        data = self._get_numeric_data()
    else:
        data = self

    if data.empty:
        if isinstance(q, (float, int)):
            return pd.Series([], name=q)
        elif isinstance(q, (list, np.ndarray)):
            return pd.DataFrame([], index=q)

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

With this correction, the quantile function will now correctly handle the case of an empty DataFrame, avoiding the ValueError during concatenation, and returning the appropriate empty output structures as expected.