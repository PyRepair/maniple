### Error Analysis
- The function `quantile` in the `DataFrame` class of `pandas` is supposed to return values at the given quantile over a requested axis.
- The error occurs during array concatenation with the message `ValueError: need at least one array to concatenate`.
- The buggy function fails to properly handle cases when the DataFrame is empty or the columns are dropped.
- The failing test case involves an empty DataFrame constructed from a date range, and the bug manifests during the quantile calculation due to incorrect handling of the empty data situation.

### Bug Cause
- The cause of the bug lies in the `_get_numeric_data()` method. When a DataFrame with only datetime data is provided, `_get_numeric_data()` doesn't retain any columns, leading to an empty DataFrame.
- As a result, subsequent operations in the quantile function on this empty DataFrame lead to the concatenation error.

### Fixing Strategy
- To address the bug, we need to modify the logic within the quantile function to handle cases where the DataFrame is empty, ensuring that the computation proceeds correctly.
- We can modify the code to ensure that appropriate checks are performed to prevent errors when handling an empty DataFrame.

### Corrected Function
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data()
    
    if data.empty:
        # Return an empty DataFrame if no numeric columns are present
        if isinstance(q, (int, float)):
            return pd.DataFrame(index=self.columns, columns=self.columns)
        return pd.DataFrame(index=q, columns=self.columns)

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

### Changes Made
- Added a check for an empty DataFrame in the `data` variable after extracting numeric data.
- If the DataFrame is empty, return an empty DataFrame with the correct columns and index based on the input `q` parameter.
- This modification ensures that the quantile function can handle empty DataFrames gracefully and prevents the concatenation error.

By implementing these changes, the corrected function should now handle cases involving an empty DataFrame without encountering the concatenation error. It aligns with the expected output values and types provided for the failing test cases.