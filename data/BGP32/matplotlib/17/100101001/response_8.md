### Bug Explanation:
The bug in the `nonsingular` function is related to how it handles the cases when the input parameters `vmin` and `vmax` are not finite values (inf or NaN). The current implementation incorrectly returns `-expander, expander` when either `vmin` or `vmax` is not finite, which is not the desired behavior.

### Bug Fix Strategy:
To fix the bug, we should modify the function to correctly handle the cases when either `vmin` or `vmax` is not finite. Instead of returning a fixed range of `-expander, expander`, we can return `-np.inf, np.inf` in such cases to represent a range without bounds.

### Corrected Function:
Here is the corrected version of the `nonsingular` function:

```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -np.inf, np.inf

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

With this corrected version, the function will return an unbounded range if either `vmin` or `vmax` is not finite, addressing the bug identified.