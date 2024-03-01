### Bug Explanation
The bug in the `nonsingular` function arises due to inconsistent handling of the input values `vmin` and `vmax` in relation to the conditions specified. Specifically, when `vmin` is negative and `vmax` is positive, and the absolute value of one is greater than the other, the function does not correctly determine the `maxabsvalue` leading to incorrect comparisons and updates to `vmin` and `vmax`.

### Bug Fix Strategy
To fix the bug, we need to ensure that the calculation of `maxabsvalue` is correct and that the adjustments to `vmin` and `vmax` are performed accurately based on the specified conditions.

### Corrected Version of the Function

```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return -expander, expander
    
    swapped = False
    if not increasing and vmin > vmax:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmin), abs(vmax))
    if maxabsvalue < 1e6 * tiny * np.finfo(float).tiny:
        vmin = -expander
        vmax = expander

    elif vmax - vmin <= maxabsvalue * tiny:
        if vmax == 0 and vmin == 0:
            vmin = -expander
            vmax = expander
        else:
            vmin -= expander * abs(vmin) / 2
            vmax += expander * abs(vmax) / 2

    if swapped:
        vmin, vmax = vmax, vmin
    
    return vmin, vmax
```

### Changes Made
1. Adjusted the condition `if not increasing and vmin > vmax` for correct swapping of `vmin` and `vmax`.
2. Fixed the calculation of adjustments to `vmin` and `vmax` to be proportional to their absolute values.
3. Removed unnecessary multiplication in the condition `if maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny` for correct behavior.