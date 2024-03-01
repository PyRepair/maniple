### Bug Explanation:
The bug occurs when trying to compute the quantile for a DataFrame with datetime data. The `_get_numeric_data` function in the buggy `quantile` function calls return an empty DataFrame when there are no numeric columns, causing an error when trying to concatenate the empty arrays.

### Bug Fix Strategy:
To fix this bug, we need to handle the case where the DataFrame has only non-numeric data (e.g., datetime columns) to avoid returning an empty DataFrame. By modifying the logic to check if there are no numeric columns before proceeding with the quantile computation, we can prevent the error.

### Corrected Function:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    """
    Return values at the given quantile over requested axis.
    """
    self._check_percentile(q)

    if numeric_only:
        data = self._get_numeric_data()
    else:
        data = self

    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    if data.empty:
        return data  # Return early if empty DataFrame to avoid errors

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

By incorporating the check for an empty DataFrame early in the function, we prevent the empty arrays being concatenated, which resolves the error when computing the quantile for a DataFrame with datetime columns.