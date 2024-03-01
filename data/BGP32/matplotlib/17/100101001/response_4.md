### Bug Explanation

The bug in the `nonsingular` function lies in the condition where it handles cases where both `vmin` and `vmax` are very close to zero (or zero) without checking the swapped condition properly. When `vmin` and `vmax` are swapped but `increasing` is set to False, the return values are not swapped back correctly, leading to incorrect output.

### Bug Fix Strategy

To fix the bug, we need to adjust the handling of the swapped values when checking for singularity and updating the `vmin` and `vmax` values. We should ensure that the `swapped` condition is considered correctly in scenarios where `increasing` is set to False.

### Corrected Function

Here is the corrected version of the `nonsingular` function:

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
            vmin -= expander * abs(vmin)
            vmax += expander * abs(vmax)

    if swapped and not increasing:
        vmin, vmax = vmax, vmin
    
    return vmin, vmax
```

### Updated Runtime Values

With the corrected function, the cases provided should now output the correct values, resolving the bug and passing the failing tests.