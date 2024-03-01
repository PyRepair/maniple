### Bug Explanation
The bug is likely occurring because the condition `maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny` is always evaluating to `False`, leading to the `elif` block not getting executed for certain cases, including the provided failing cases. This leads to the function not expanding the interval when it is too small.

### Bug Fix Strategy
To fix the bug, we need to modify the condition that checks if the interval is too small to correctly trigger the interval expansion block.

### Corrected Function
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    if vmax < vmin:
        vmin, vmax = vmax, vmin

    maxabsvalue = max(abs(vmin), abs(vmax))
    if maxabsvalue < tiny:
        vmin = -expander
        vmax = expander

    elif vmax - vmin <= maxabsvalue * tiny:
        if vmax == 0 and vmin == 0:
            vmin = -expander
            vmax = expander
        else:
            vmin -= expander*abs(vmin)
            vmax += expander*abs(vmax)

    if not increasing and vmax < vmin:
        vmin, vmax = vmax, vmin
    return vmin, vmax
```

The corrected function adjusts the condition `if maxabsvalue < tiny` to compare directly with `tiny` instead of a calculated value involving `1e6`. This change should correctly trigger the interval expansion when the interval is too small, addressing the bug.