### Bug Explanation:
The bug occurs when both `vmin` and `vmax` are finite but `vmax < vmin` due to incorrect checking in the function. This leads to the swapping of the values even when they are both finite, resulting in incorrectly transposed values.

### Bug Fix:
To fix the bug, we need to modify the logic to only swap `vmin` and `vmax` if one of them is not finite. We should only swap the values if necessary to ensure `vmin` is less than or equal to `vmax` when both are finite.

### Corrected Version of the Function:
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
        the original interval is too small, based on *tiny.
    tiny : float, default: 1e-15
        Threshold for the ratio of the interval to the maximum absolute
        value of its endpoints. If the interval is smaller than
        this, it will be expanded. This value should be around
        1e-15 or larger; otherwise the interval will be approaching
        the double precision resolution limit.
    increasing : bool, default: True
        If True, swap *vmin*, *vmax* if *vmin* > *vmax.

    Returns
    -------
    vmin, vmax : float
        Endpoints, expanded and/or swapped if necessary.
        If either input is inf or NaN, or if both inputs are 0 or very
        close to zero, it returns -*expander*, *expander.
    """

    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    if increasing and vmax < vmin:
        vmin, vmax = vmax, vmin

    maxabsvalue = max(abs(vmin), abs(vmax))
    if maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:
        vmin = -expander
        vmax = expander

    elif vmax - vmin <= maxabsvalue * tiny:
        if vmax == 0 and vmin == 0:
            vmin = -expander
            vmax = expander
        else:
            vmin -= expander * abs(vmin)
            vmax += expander * abs(vmax)

    return vmin, vmax
```

By correcting the swapping logic and only swapping when necessary, the function should now handle the cases where both `vmin` and `vmax` are finite values correctly.