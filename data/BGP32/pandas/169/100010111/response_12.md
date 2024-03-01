Explanation:
The bug is caused by the `_get_numeric_data()` method returning an empty DataFrame when the input DataFrame contains datetime data, which leads to an attempt to concatenate empty arrays later in the function.

Strategy for fixing the bug:
1. Check if the provided data is numeric before using `_get_numeric_data()`.
2. If the data is numeric, extract the necessary data; otherwise, use the entire DataFrame.

To address the bug, we need to modify the function to handle the case when `_get_numeric_data()` doesn't return any data and ensure that the subsequent computations receive valid data.

Here is the corrected version of the function:

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
        when the desired quantile lies between two data points `i` and `j`.

    Returns
    -------
    Series or DataFrame

    See Also
    --------
    core.window.Rolling.quantile: Rolling quantile.
    numpy.percentile: Numpy function to compute the percentile.
    """
    
    # Check if the data is numeric to avoid empty DataFrame
    if numeric_only:
        data = self._get_numeric_data()
        if data.empty:
            data = self
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

This corrected version of the function will handle the input DataFrame containing datetime data correctly and avoid the ValueError related to concatenating empty arrays during computation.