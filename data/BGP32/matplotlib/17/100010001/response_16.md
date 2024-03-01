### Analysis
The error messages indicate that there are overflow warnings when performing arithmetic operations in the `nonsingular` function. The errors occur specifically when calculating the difference between `vmax` and `vmin`, and when calculating the absolute value of `vmin` and `vmax`.

### Bug Cause
The bug is caused by using integer values (`-20000`, `20000`, `-32768`, `0`) as arguments for `vmin` and `vmax` in the `test_colorbar_int` test function. Due to the calculations involving these integer values, overflow warnings are raised by the `nonsingular` function when trying to perform operations that exceed the range of integers.

### Fix Strategy
To fix the bug, we need to ensure that the values for `vmin` and `vmax` in the `nonsingular` function are floating-point numbers. This way, we can avoid overflow issues when performing arithmetic operations. We can simply convert the integer values to floating-point values before passing them to the `nonsingular` function.

### Corrected Version
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
    
    vmin, vmax = float(vmin), float(vmax)  # Convert values to float
    
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander
    
    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True
    
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
    
    if swapped and not increasing:
        vmin, vmax = vmax, vmin
    return vmin, vmax
```

By converting the `vmin` and `vmax` values to floating-point numbers at the beginning of the function, we ensure that the subsequent calculations won't run into overflow issues when dealing with integer inputs.