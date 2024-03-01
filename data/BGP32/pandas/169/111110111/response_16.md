### Bug Analysis:
1. The `DataFrame.quantile()` function tries to compute the quantiles over requested axis for the input DataFrame object.
2. The function expects parameters such as `q` (quantile value), `axis` (row/column-wise quantile calculation), `numeric_only` (whether to consider only numeric data), and `interpolation` (method for interpolation when calculating quantiles).
3. The failing test case `test_quantile_empty_no_columns` creates a DataFrame with only DateTime data and tries to calculate the quantile, leading to the `ValueError: need at least one array to concatenate` error.
4. The root cause of the failure seems to be related to the form of the input data, specifically handling DateTime data during the quantile computation.
5. The expected outputs of the function should correctly handle the DateTime data input, just like Series objects.

### Bug Fix Strategy:
1. Update the function implementation to appropriately handle cases when all columns are dropped due to having non-numeric data.
2. Ensure that the quantile calculation for non-numeric data (like DateTime) is handled correctly.
3. Address the concatenation issue that leads to the `ValueError`.

### Corrected Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    """
    Return values at the given quantile over the requested axis.

    Parameters
    ----------
    q : float or array-like, default 0.5 (50% quantile)
        Value between 0 <= q <= 1, the quantile(s) to compute.
    axis : {0, 1, 'index', 'columns'} (default 0)
        Equals 0 or 'index' for row-wise, 1 or 'columns' for column-wise.
    numeric_only : bool, default True
        If False, the quantile of datetime and timedelta data will be computed as well.
    interpolation : {'linear', 'lower', 'higher', 'midpoint', 'nearest'}
        This optional parameter specifies the interpolation method to use when the desired quantile lies between two data points.

    Returns
    -------
    Series or DataFrame
    """
    self._check_percentile(q)

    data = self._get_numeric_data() if numeric_only else self.select_dtypes(include=np.number)
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if not data.empty:
        index = data.index if not is_transposed else data.columns
        cols = data.columns if not is_transposed else data.index

    result = data._data.quantile(q, axis=1, interpolation=interpolation, transposed=is_transposed)

    if result.ndim == 2:
        result = self._constructor(result, index=index, columns=cols)
    else:
        result = self._constructor_sliced(result, name=q, index=index)

    if is_transposed:
        result = result.T

    return result
```

### Modification Remarks:
1. `select_dtypes(include=np.number)` is used to filter only numeric data if `numeric_only=False`.
2. Handling for empty DataFrame cases, ensuring appropriate index and column handling.
3. Updated DataFrame construction with the correct index and columns.
4. Adjusted quantile calculation and result formatting.

By applying these modifications, the corrected function should address the issue and provide the expected outputs during the failing test scenario.