### Bug Explanation
The bug in the `nonsingular` function arises from the condition `elif vmax - vmin <= maxabsvalue * tiny` that is supposed to handle cases where the difference between `vmax` and `vmin` is very small. However, the bug occurs when both `vmax` and `vmin` are equal to zero, where the condition `vmax - vmin <= maxabsvalue * tiny` evaluates to `True` leading to an incorrect calculation of `vmin` and `vmax` by subtracting and adding `expander` respectively.

### Bug Fix Strategy
To fix the bug, we need to explicitly check if both `vmin` and `vmax` are zero before applying the adjustment. In the case where both are zero, we should set `vmin` to `-expander` and `vmax` to `expander` directly without the extra calculation.

### Corrected Function
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

By incorporating the explicit check for when both `vmin` and `vmax` are zero, we ensure that the function correctly handles this scenario and adjusts the values accordingly. This corrected version should now pass the failing test cases provided.