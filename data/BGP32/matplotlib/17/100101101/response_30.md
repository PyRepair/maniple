### Bug Explanation
The bug in the `nonsingular` function lies in the condition that checks whether the interval between `vmin` and `vmax` is smaller than a certain threshold (`maxabsvalue * tiny`) and needs to be expanded. In Case 2 and Case 3, the condition `vmax - vmin <= maxabsvalue * tiny` is incorrectly taking into account the absolute difference between `vmax` and `vmin` instead of just the difference. This leads to incorrect expansion and swapping behavior of the endpoints, causing the failing tests.

### Bug Fix Strategy
To fix the bug, we need to modify the condition `vmax - vmin <= maxabsvalue * tiny` to just check the difference between `vmax` and `vmin`, disregarding their absolute values.

### Corrected Function
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmin), abs(vmax))
    if maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:
        vmin = -expander
        vmax = expander

    diff = vmax - vmin
    if diff <= maxabsvalue * tiny:
        if diff == 0:
            vmin = -expander
            vmax = expander
        else:
            vmin -= expander * diff / 2
            vmax += expander * diff / 2

    if swapped and not increasing:
        vmin, vmax = vmax, vmin
    return vmin, vmax
```

By making the adjustment to use `diff` instead of `vmax - vmin`, the corrected function should now pass the failing tests and correctly handle the expansion and swapping of endpoints.