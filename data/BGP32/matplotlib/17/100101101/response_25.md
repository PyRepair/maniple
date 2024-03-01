### Bug Explanation
The bug in the `nonsingular` function stems from the condition to handle very small intervals. When the difference between `vmax` and `vmin` is less than or equal to `maxabsvalue * tiny`, the function should adjust the endpoints to avoid singularities. However, the current implementation doesn't handle this case correctly and leads to incorrect results.

### Bug Fix Strategy
To fix the bug, we need to update the logic in the `nonsingular` function to properly adjust the endpoints when the interval is very small. Specifically, we need to properly handle scenarios where `vmax - vmin` is less than or equal to `maxabsvalue * tiny`.

### Corrected Code
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmin), abs(vmax))
    interval = vmax - vmin
    if interval < maxabsvalue * tiny:
        if vmin == vmax == 0:
            vmin, vmax = -expander, expander
        else:
            vmin = (vmin - expander) if vmin < 0 else (vmin + expander)
            vmax = (vmax - expander) if vmax < 0 else (vmax + expander)

    if swapped and not increasing:
        vmin, vmax = vmax, vmin

    return vmin, vmax
```

The corrected code now properly handles cases where the interval is very small and adjusts the endpoints accordingly to avoid singularities. This updated logic should pass the failing test cases and satisfy the expected input/output values.