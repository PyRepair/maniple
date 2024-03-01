### Bug Explanation
The bug occurs because the original implementation of the `nonsingular` function does not correctly handle the case when one of the inputs is `-inf` and the other is `inf`. The current implementation incorrectly returns `-expander, expander` for both `-inf` and `inf`, which is not the correct behavior.

### Bug Fix Strategy
To fix the bug, we need to modify the implementation to correctly handle the case when one input is `-inf` and the other is `inf`. We should return `vmin, vmax` directly in this scenario.

### Corrected Version of the `nonsingular` function
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return vmin, vmax

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

After applying this fix, the `nonsingular` function should now handle the case when one input is `-inf` and the other is `inf` correctly and pass the failing test cases.