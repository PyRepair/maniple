### Bug Explanation:
The bug in the `nonsingular` function is related to handling values close to the double precision resolution limit. In particular, when the interval between `vmin` and `vmax` is very small (less than a certain threshold based on `tiny`) the function tries to expand the interval, resulting in incorrect values. Additionally, there is a inconsistency in handling non-finite values.

### Bug Fix Strategy:
1. Ensure that non-finite values (inf, NaN) are handled correctly.
2. Check if the interval is very small and adjust the endpoints accordingly.
3. Confirm that the `swapped` condition is correctly considered.
4. Update the function to properly handle the cases where both inputs are 0 or very close to zero.

### Corrected Function:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    """
    Modify the endpoints of a range as needed to avoid singularities.

    Parameters
    ----------
    vmin, vmax : float
        The initial endpoints.
    expander : float, default: 0.001
        Fractional amount by which *vmin* and *vmax* are expanded if
        the original interval is too small, based on *tiny*.
    tiny : float, default: 1e-15
        Threshold for the ratio of the interval to the maximum absolute
        value of its endpoints.  If the interval is smaller than
        this, it will be expanded.  This value should be around
        1e-15 or larger; otherwise the interval will be approaching
        the double precision resolution limit.
    increasing : bool, default: True
        If True, swap *vmin*, *vmax* if *vmin* > *vmax*.

    Returns
    -------
    vmin, vmax : float
        Endpoints, expanded and/or swapped if necessary.
        If either input is inf or NaN, or if both inputs are 0 or very
        close to zero, it returns -*expander*, *expander*.
    """

    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return -expander, expander

    if vmax < vmin:
        vmin, vmax = vmax, vmin

    maxabsvalue = max(abs(vmin), abs(vmax))
    if maxabsvalue == 0 or (vmax - vmin) <= maxabsvalue * tiny:
        vmin = -expander
        vmax = expander
    else:
        vmin -= expander * abs(vmin)
        vmax += expander * abs(vmax)

    if not increasing:
        vmin, vmax = vmax, vmin

    return vmin, vmax
```

By making the above corrections, the `nonsingular` function should now handle the specified test cases correctly.