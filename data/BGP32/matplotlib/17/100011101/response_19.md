## Bug Explanation
The bug in the `nonsingular` function arises from the computation involving `maxabsvalue = max(abs(vmin), abs(vmax))` when either `vmin` or `vmax` is set to values that may lead to overflow errors or incorrect absolute computations. This bug becomes evident when handling extreme values such as `-inf`, `inf`, or values close to the limits of `int16`.

By taking the absolute value of such extreme inputs without proper handling, overflow warnings can be triggered during the computation of `maxabsvalue`, leading to potential incorrect results. Additionally, the logic related to swapping of values might be disturbed if the swapping is done incorrectly.

## Bug Fix Strategy
1. Handle extreme and infinite values such as `-inf` and `inf` separately to avoid overflow issues.
2. Update the computation of `maxabsvalue` to account for potential overflow scenarios and ensure correct results.
3. Check the logic for swapping to make sure it behaves correctly.
4. Consider the representation of values to ensure consistency and correctness in floating-point computations.

## Corrected Version of the Function
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

    if np.isinf(vmin) or np.isinf(vmax) or np.isnan(vmin) or np.isnan(vmax) or (vmin == 0 and vmax == 0):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    if np.abs(vmin) > np.abs(vmax):
        maxabsvalue = vmin
    else:
        maxabsvalue = vmax

    if maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:
        vmin = -expander
        vmax = expander
        
    elif vmax - vmin <= maxabsvalue * tiny:
        vmin -= expander * np.abs(vmin)
        vmax += expander * np.abs(vmax)
    
    if swapped and not increasing:
        vmin, vmax = vmax, vmin
    
    return vmin, vmax
```

With the corrected version of the `nonsingular` function, the issues related to handling extreme and infinite values, overflow errors, and incorrect computations should be resolved. The function should now provide the expected results for the given test cases.