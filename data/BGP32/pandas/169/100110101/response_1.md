### Bug Analysis
- The failing test `test_quantile_empty_no_columns` creates a DataFrame `df` containing a date range and sets the column name to "captain tightpants".
- The test then calls the `quantile` function on this DataFrame with `q=0.5`.
- The error message indicates a `ValueError: need at least one array to concatenate`, suggesting an issue with concatenation in the `quantile` function.
- The expected values show that the `data` DataFrame inside the function becomes an empty DataFrame, leading to the concatenation error when trying to calculate the quantile.

### Bug Fix Strategy
- The function should check if the data DataFrame is empty after filtering numeric data. If empty, it should return an empty Series or DataFrame depending on the input `q`.
- Handle the case of empty data properly to avoid errors during quantile calculation.

### Corrected Function
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data()
    if data.empty:
        if isinstance(q, list):
            return pd.DataFrame(index=q, columns=[])
        else:
            return pd.Series([], index=[], name=q)

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

By checking for empty data and returning the appropriate empty Series or DataFrame before proceeding with the quantile calculation, we ensure that the function handles such cases correctly and avoids errors.