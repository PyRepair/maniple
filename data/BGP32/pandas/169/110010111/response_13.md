### Issue Analysis
1. **Buggy function and class relationship**: The buggy function `quantile` is a method within the `DataFrame` class, which is used to calculate the quantile values for the DataFrame along the specified axis.
   
2. **Error Message**: The error message indicates a `ValueError` due to needing at least one array to concatenate. This might be related to the expected input values not being correctly processed within the function.
   
3. **Expected Input/Output**: The function is expected to return quantile values for a DataFrame with datetime data, similar to the behavior when used with Series data.

4. **GitHub Issue**: The reported issue explains that while `pd.Series(pd.date_range('1/1/18', periods=5)).quantile()` works fine, the equivalent using a DataFrame raises a `ValueError`, indicating a bug.

### Bug Fix Strategy
The bug seems to be related to the incorrect processing of data when no numeric data is present in the DataFrame. To fix this bug, we need to adjust the logic in the function to handle scenarios where no numeric data exists in the DataFrame.

### Corrected Function
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

        * linear: `i + (j - i) * fraction`, where `fraction` is the
          fractional part of the index surrounded by `i` and `j`.
        * lower: `i`.
        * higher: `j`.
        * nearest: `i` or `j` whichever is nearest.
        * midpoint: (`i` + `j`) / 2.

    Returns
    -------
    Series or DataFrame

        If ``q`` is an array, a DataFrame will be returned where the
          index is ``q``, the columns are the columns of self, and the
          values are the quantiles.
        If ``q`` is a float, a Series will be returned where the
          index is the columns of self and the values are the quantiles.
    """
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if data.empty:
        return pd.DataFrame() if isinstance(q, (float, int)) else pd.Series()

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

This corrected function includes a check for empty data frames and returns an empty DataFrame for float or int `q`, or an empty Series for array-like `q`. This adjustment should resolve the issue and ensure the function handles different cases appropriately.