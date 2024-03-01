### Analysis:
1. The buggy function is `quantile` in the `pandas/core/frame.py` file.
2. The failing test is `test_quantile_empty_no_columns` in the `pandas/tests/frame/test_quantile.py` file.
3. The error message indicates a `ValueError: need at least one array to concatenate`.
4. The bug seems to be related to the `concat_compat` function in the `pandas/core/dtypes/concat.py` file when trying to concatenate values.
   
### Bug Explanation:
The bug occurs because the `_get_numeric_data()` function may end up dropping all columns, resulting in an empty DataFrame. This empty DataFrame is then passed to the `quantile` function, where an attempt is made to concatenate the values. Since there are no values to concatenate, a `ValueError` is raised.

### Strategy for Fixing the Bug:
To fix the bug, we need to ensure that the DataFrame passed to the `quantile` function contains at least one column. One way to address this is to modify the `quantile` function to check if the DataFrame is empty after filtering out non-numeric columns using `_get_numeric_data()`. If the DataFrame becomes empty, an appropriate action can be taken to handle this scenario, such as returning an empty Series or DataFrame.

### Corrected Version of the Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    """
    Return values at the given quantile over requested axis.
    """

    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self

    # Check if the resulting DataFrame is empty
    if data.empty:
        if isinstance(q, float):
            # Return an empty Series
            return pd.Series([], index=data.columns, name=q)
        else:
            # Return an empty DataFrame
            return pd.DataFrame([], index=q, columns=data.columns)

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

By checking for an empty DataFrame after filtering out non-numeric columns, the corrected function will handle cases where an empty DataFrame is encountered, thus preventing the `ValueError` during concatenation.