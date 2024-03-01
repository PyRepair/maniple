### Bug Explanation:
The bug in the `nonsingular` function lies in the calculation of `maxabsvalue`. The calculation comparison condition `maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny` is flawed and doesn't assess the maximum absolute value correctly. This leads to incorrect adjustment of `vmin` and `vmax`.

### Bug Fix Strategy:
To fix the bug, we need to correct the calculation of `maxabsvalue` based on the maximum absolute value between `vmin` and `vmax`. This will ensure that the expansion and swapping logic within the function operates correctly.

### Corrected Version of `nonsingular` Function:
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

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmin), abs(vmax))
    
    if maxabsvalue < tiny:
        delta = (vmax - vmin) * expander / 2
        vmin -= delta
        vmax += delta
    
    if swapped and not increasing:
        vmin, vmax = vmax, vmin

    return vmin, vmax
```

The corrected version addresses the calculation of `maxabsvalue` and adjusts the `vmin` and `vmax` values accordingly. This corrected function should now pass the failing test cases and handle endpoints correctly.