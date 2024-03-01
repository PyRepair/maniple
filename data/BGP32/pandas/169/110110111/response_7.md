### Bug Explanation

The bug in the `DataFrame.quantile` function arises from the creation of an empty DataFrame when no columns are present after the initial data operation. This empty DataFrame leads to the `ValueError: need at least one array to concatenate` error during quantile computation.

The failing test in `test_quantile_empty_no_columns` creates a DataFrame with columns generated from `pd.date_range("1/1/18", periods=5)` resulting in a DataFrame with no columns, only an index. When the `quantile` function is called on this DataFrame, it attempts to compute the quantile with an empty DataFrame, causing the ValueError.

### Bug Fix Strategy

To fix the bug:
1. Ensure that if the DataFrame becomes empty after identifying numeric data (`_get_numeric_data()`), it should not attempt to continue with the quantile computation.
2. Handle the case where no columns are present in the DataFrame gracefully to prevent concatenation errors.

### Corrected Function

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self

    if len(data.columns) == 0:  # Check for empty DataFrame after numeric data filtering
        return self._constructor()

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

With this correction, the function will exit early and return an empty DataFrame if no columns are present in the DataFrame after filtering for numeric data. This will prevent the concatenation error and ensure that the quantile computation proceeds correctly.