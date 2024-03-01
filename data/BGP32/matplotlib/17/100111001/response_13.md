### Bug Explanation
The bug in the `nonsingular` function arises when calculating `maxabsvalue` using the `max` function with `abs(vmin)` and `abs(vmax)`. In Case 3 when `vmin = 0.5` and `vmax = -0.5`, after the `if` condition where `vmin` and `vmax` are swapped, the `maxabsvalue` incorrectly becomes `0.5` instead of `0.5` since `vmin` and `vmax` are swapped but the absolute values are not updated accordingly. This leads to incorrect calculations in further steps.

### Bug Fix Strategy
To fix the bug, we need to make sure that `maxabsvalue` reflects the correct maximum absolute value of `vmin` and `vmax` regardless of their order after the swap. One way to achieve this is to calculate `maxabsvalue` after the potential swap has been performed so that it always captures the correct maximum value.

### Corrected Version of the Function
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander
    
    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True
    
    maxabsvalue = max(abs(vmin), abs(vmax))  # Calculate maximum absolute value after the potential swap
    
    if maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:
        vmin = -expander
        vmax = expander
    
    elif vmax - vmin <= maxabsvalue * tiny:
        if vmax == 0 and vmin == 0:
            vmin = -expander
            vmax = expander
        else:
            vmin -= expander*abs(vmin)
            vmax += expander*abs(vmax)
    
    if swapped and not increasing:
        vmin, vmax = vmax, vmin
    return vmin, vmax
```

By recalculating `maxabsvalue` after the potential swap, the corrected function should now handle cases where `vmin` and `vmax` are swapped correctly, ensuring the correct maximum absolute value is used throughout the function's logic.