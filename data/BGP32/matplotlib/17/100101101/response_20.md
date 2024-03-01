### Bug Analysis:
The `nonsingular` function is failing to handle boundary cases correctly when adjusting the `vmin` and `vmax` values to avoid singularities. The bug is likely related to the conditional checks and adjustments made within the function. Specifically, when `vmax - vmin` is very small, the function should expand the range, but the current implementation might not be doing this correctly.

### Bug Fix Strategy:
To address the bug, we need to ensure that the condition checks and adjustments within the function are correctly handling scenarios where the input endpoints are very close to each other or approaching zero. We should also make sure that the adjustments respect the direction of the range and that swapping occurs properly when needed.

### Corrected Function:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
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

    elif abs(vmax - vmin) <= maxabsvalue * tiny:
        if vmax == 0 and vmin == 0:
            vmin = -expander
            vmax = expander
        else:
            direction = 1 if increasing else -1
            vmin -= direction * expander * abs(vmin)
            vmax += direction * expander * abs(vmax)

    if swapped and not increasing:
        vmin, vmax = vmax, vmin

    return vmin, vmax
```

By modifying the adjustment calculation when the range is too small, considering the direction of the range based on the `increasing` parameter, and ensuring proper swapping, we can address the issues causing the failing tests. The corrected function aims to handle singular boundary cases more effectively.