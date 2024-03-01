### Analysis:
- The buggy function `quantile` in the `pandas/core/frame.py` file is supposed to return values at the given quantile over the requested axis. 
- The failing test `test_quantile_empty_no_columns` in `pandas/tests/frame/test_quantile.py` checks if the quantile computation works correctly with empty columns.
- The error message indicates a `ValueError: need at least one array to concatenate`.
- The GitHub issue titled "DataFrame Quantile Broken with Datetime Data" describes a scenario where quantile computation with a DataFrame fails while it works fine with a Series.

### Bug Description:
- The bug occurs because when the `quantile` function is called with `numeric_only=True`, the function later attempts to concatenate arrays from blocks even if they are empty, leading to the `ValueError`.
- The failing case from the test function passes an empty DataFrame with a date-range object, triggering this issue.

### Fix Strategy:
- Check for the presence of data in the numeric columns before proceeding with block concatenation.
- Modify the logic to handle empty columns gracefully and prevent the concatenation operation from raising a `ValueError`.

### Code Fix:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)
    
    data = self._get_numeric_data() if numeric_only and not self.empty else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    if data.empty:
        if isinstance(q, list):
            result = pd.DataFrame([], index=q, columns=data.columns)
        else:
            result = pd.Series([], index=data.columns, name=q)
    else:
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

By implementing this fix, the `quantile` function will now handle cases where the DataFrame is empty or has no numeric columns gracefully, preventing the `ValueError` during block concatenation. This corrected version should pass the failing test and resolve the issue reported on GitHub.