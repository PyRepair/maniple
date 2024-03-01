### Explanation:
The error message indicates a `ValueError: need at least one array to concatenate`. This error occurs during concatenation in the `_concat_compat` function in `pandas/core/dtypes/concat.py`. It suggests that there are no valid arrays to concatenate when attempting to merge data for quantile computation.

The bug arises from `_get_numeric_data()` function that may drop all columns if they contain non-numeric data like datetime. When passing datetime data to the `quantile` function in a DataFrame, without specifying `numeric_only=False`, all columns may be removed due to the nature of the `_get_numeric_data()` operation.

### Bug Fix Strategy:
Modify the function to check if `numeric_only` is set to `True`. If `True`, then proceed with only numeric data processing. If `False`, include datetime and timedelta data when calculating quantiles.

### Corrected Code:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    """
    Return values at the given quantile over requested axis.

    Parameters
    ----------
    q : float or array-like, default 0.5 (50% quantile)
        Value between 0 <= q <= 1, the quantile(s) to compute.
    axis : {0, 1, 'index', 'columns'} (default 0)
        Equals 0 or 'index' for row-wise, 1 or 'columns' for column-wise.
    numeric_only : bool, default True
        If False, the quantile of datetime and timedelta data will be
        computed as well.
    interpolation : {'linear', 'lower', 'higher', 'midpoint', 'nearest'}
        This optional parameter specifies the interpolation method to use,
        when the desired quantile lies between two data points `i` and `j`:
        ...
    Returns
    -------
    Series or DataFrame
        ...

    Examples
    --------
    ...

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

This corrected version of the function includes a check for `numeric_only` parameter to determine whether to include all data types or only numeric data when computing quantiles, thereby addressing the issue of dropping all columns due to non-numeric data.