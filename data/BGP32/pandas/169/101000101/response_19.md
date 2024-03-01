The bug in the function arises from incorrect handling of the "qs" parameter (quantiles) for the quantile calculation. The buggy function attempts to call self._check_percentile(q), but the correct usage should be self._check_percentile([q]), as the function expects "qs" to be an array-like object.

To fix the bug:
1. Update the parameter q in the function signature to qs.
2. Pass [q] instead of q to the _check_percentile method.
3. Ensure that if qs is a float, it is converted to a list containing that float before passing it to _check_percentile.

Here is the corrected version of the function:

```python
def quantile(self, qs=0.5, axis=0, numeric_only=True, interpolation="linear"):
    """
    Return values at the given quantile over requested axis.
    """

    self._check_percentile([qs])

    data = self._get_numeric_data() if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    result = data._data.quantile(
        qs=qs, axis=1, interpolation=interpolation, transposed=is_transposed
    )

    if result.ndim == 2:
        result = self._constructor(result)
    else:
        result = self._constructor_sliced(result, name=qs)

    if is_transposed:
        result = result.T

    return result
```

With these corrections, the function should now correctly handle the quantile calculation for both single float quantiles and array-like quantiles.