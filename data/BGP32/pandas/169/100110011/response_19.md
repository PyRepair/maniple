### Issue Analysis:
1. The `quantile` function in `pandas/core/frame.py` is failing when `df = pd.DataFrame(pd.date_range("1/1/18", periods=5))` is used.
2. The test case `test_quantile_empty_no_columns` in `pandas/tests/frame/test_quantile.py` is testing this failure for the `quantile` function.
3. The error message indicates a `ValueError: need at least one array to concatenate`.
4. The GitHub issue `DataFrame Quantile Broken with Datetime Data` corresponds to this bug and specifies that the DataFrame quantile does not work with datetime data.
  
### Error Cause:
The cause of the bug is that when `df` contains only datetime data, the data is not considered numeric, and the method to extract numeric data does not handle the case where all columns are dropped. This results in an empty DataFrame that causes the concatenation error.

### Bug Fix Strategy:
To fix this bug:
1. Check if the DataFrame has numeric data before attempting to extract it.
2. Handle the case where no numeric columns remain after extraction.
3. Ensure that the resulting Series/DataFrame maintains the correct structure even if there are no numeric columns to compute the quantile from.

### Corrected Function:
Here is the corrected version of the `quantile` function in the `pandas/core/frame.py` file:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only and self._get_numeric_data().shape[1] != 0 else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    if numeric_only and self._get_numeric_data().shape[1] == 0:
        result = pd.DataFrame([], index=[q] if isinstance(q, float) else q, columns=self.columns)
    else:
        result = data._data.quantile(qs=q, axis=1, interpolation=interpolation, transposed=is_transposed)

    if result.ndim == 2:
        result = self._constructor(result)
    else:
        result = self._constructor_sliced(result, name=q)

    if is_transposed:
        result = result.T

    return result
```

This corrected version of the `quantile` function checks for the presence of numeric data columns and handles the case where no numeric columns are left due to dropping them. It ensures the output maintains the expected structure even when dealing with datetime data.