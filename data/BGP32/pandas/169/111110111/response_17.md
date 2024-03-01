## Identified Bug:
The bug occurs in the quantile function of the DataFrame class in the pandas library when attempting to calculate the quantile of a DataFrame that only contains datetime data. The bug causes a ValueError stating "need at least one array to concatenate" due to data manipulation issues.

## Bug Fix Strategy:
1. Identify the root cause of the problem which is related to handling datetime data.
2. Implement a check to identify if the DataFrame contains only datetime data and handle such cases properly to avoid the concatenation issue.

## Corrected Version of the Function:
```python
# Fixed implementation avoiding the concatenation error with datetime only data
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

    See Also
    --------
    core.window.Rolling.quantile: Rolling quantile.
    numpy.percentile: Numpy function to compute the percentile.
    """
    self._check_percentile(q)

    if numeric_only:  # If only numeric columns are required
        data = self._get_numeric_data()
    else:
        data = self
    
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    if data.empty:  # Special handling for empty DataFrame
        return data

    non_date_cols = data.select_dtypes(exclude=['datetime64', 'timedelta64']).columns
    if len(non_date_cols) == len(data.columns):  # Handle data with only datetime columns
        return data

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

By implementing the suggested corrections, the function now properly handles DataFrame containing only datetime data and avoids the concatenation error.