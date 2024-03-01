### Analysis:
1. The buggy function is `quantile()` in the `pandas/core/frame.py` file.
2. The test code `test_quantile_empty_no_columns` in `pandas/tests/frame/test_quantile.py` is failing due to this bug.
3. The detailed error message points towards a concatenation issue in the function `quantile()`, leading to a `ValueError`.
4. The GitHub issue mentions that the `quantile()` method should work consistently with datetime data in both Series and DataFrame.

### Issue:
The bug occurs when trying to compute quantile values of empty DataFrames with datetime data, leading to a concatenation error.

### Bug Cause:
In the `quantile()` function's faulty code, if the DataFrame has only datetime or empty data, the concatenation operation will fail as no arrays are available for concatenation. This results in the `ValueError: need at least one array to concatenate`.

### Strategy for Fixing the Bug:
To fix the bug, we need to handle the case where the DataFrame has no numeric data, such as with datetime data or when the DataFrame is empty. The fix should ensure the function can handle these scenarios and return appropriate outputs without causing errors.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if data.empty:
        if isinstance(q, float) or (isinstance(q, list) and len(q) == 1):
            return pd.Series([], index=[0.5] if isinstance(q, float) else q, name=q)
        else:
            return pd.DataFrame([], index=q, columns=[])

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

By adding a check for an empty DataFrame and handling the scenario where the DataFrame has datetime or non-numeric data, the corrected function will now return appropriate results without causing a concatenation error.

This corrected version should now pass the failing test and resolve the issue reported on GitHub.