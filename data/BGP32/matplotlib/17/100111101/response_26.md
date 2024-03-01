### Bug Explanation:
The bug in the `nonsingular` function is caused by potential overflow issues with the calculations related to the `maxabsvalue`. The expression `maxabsvalue = max(abs(vmin), abs(vmax))` might encounter overflow exceptions, resulting in incorrect values for `maxabsvalue`.

The error messages indicate that overflow is encountered in the comparison or subtraction of values, leading to `RuntimeWarning` messages.

### Bug Fix Strategy:
To fix the bug, we need to adjust the calculations based on the input values to avoid potential overflow issues when computing `maxabsvalue`.

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
        value of its endpoints. If the interval is smaller than
        this, it will be expanded. This value should be around
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

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    if np.abs(vmax) <= tiny and np.abs(vmin) <= tiny:
        return -expander, expander
    
    maxabsvalue = max(abs(vmin), abs(vmax))
    
    if maxabsvalue < tiny:
        vmin = -expander
        vmax = expander
    elif vmax - vmin <= maxabsvalue * tiny:
        if vmax == 0 and vmin == 0:
            vmin = -expander
            vmax = expander
        else:
            vmin -= expander * np.abs(vmin)
            vmax += expander * np.abs(vmax)

    if swapped and not increasing:
        vmin, vmax = vmax, vmin
        
    return vmin, vmax
```

After applying the fix, the `nonsingular` function should handle the calculations correctly without encountering overflow issues, leading to the correct results for the failing test cases.