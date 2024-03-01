### Bug Explanation
The bug occurs in the DataFrame method `quantile()` when it encounters a DataFrame that contains only datetime data. The issue is with the implementation of handling empty DataFrames while generating quantiles, which leads to concatenation errors due to the lack of arrays to concatenate.

When the DataFrame consists entirely of datetime data and the `quantile()` method is invoked, it results in an attempt to concatenate empty DataFrames causing the `ValueError: need at least one array to concatenate`.

### Bug Fix Strategy
To fix this bug, we need to ensure that the function handles such edge cases correctly. It should check if the DataFrame contains any data after the filtering based on `numeric_only`. If the DataFrame is empty, the function should return an empty DataFrame/series accordingly.

### Corrected Function
Here is the corrected version of the `quantile()` function:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self

    if len(data) == 0:
        if isinstance(q, (list, np.ndarray)):
            return self._constructor_sliced([], index=q)
        else:
            return pd.Series([], index=self.columns, name=q)

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

This corrected version includes handling the case where the `data` DataFrame is empty after the filtering based on `numeric_only`. If the DataFrame is empty, the function will directly return an empty DataFrame or Series based on the type of `q`. This approach ensures that the function can handle empty DataFrame cases without causing concatenation errors.