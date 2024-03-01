### Bugs Identified:
1. The condition `elif vmax - vmin <= maxabsvalue * tiny:` is not correctly handling the case where both `vmax` and `vmin` are 0. It should be `elif vmax - vmin <= maxabsvalue * tiny and vmax != 0 and vmin != 0:`
2. The condition `maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:` should use `np.finfo(float).tiny` instead of `np.finfo(float).tiny`.

### Bug Explanation:
1. In Case 3, when `vmin = 0.5` and `vmax = -0.5`, it correctly swaps the values due to `vmax < vmin`. Then, inside the condition `elif vmax - vmin <= maxabsvalue * tiny:`, it incorrectly enters the block intended for small intervals, even though in this case, both `vmax` and `vmin` are non-zero. This leads to incorrect adjustments of `vmin` and `vmax`.

2. In Case 4, when `vmin = -inf` and `vmax = inf`, the function should return `-expander, expander` due to the conditions in the beginning of the function. However, it doesn't handle this case correctly.

### Bug Fix Strategy:
1. Modify the condition `elif vmax - vmin <= maxabsvalue * tiny:` to include additional checks for `vmax != 0` and `vmin != 0`.
2. Replace `np.finfo(float).tiny` in the condition `maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:` with `np.finfo(float).tiny`.

### Corrected Version of the Function:
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

    elif vmax - vmin <= maxabsvalue * tiny and vmax != 0 and vmin != 0:
        vmin -= expander*abs(vmin)
        vmax += expander*abs(vmax)

    if swapped and not increasing:
        vmin, vmax = vmax, vmin
    return vmin, vmax
```

With these fixes, the corrected function should now handle the edge cases correctly and pass the failing test cases.