### Bug Explanation:
The bug in the `nonsingular` function arises from the conditional check:
```python
elif vmax - vmin <= maxabsvalue * tiny:
```
This line is attempting to check if the difference between `vmax` and `vmin` is within a certain small range defined by `maxabsvalue` and `tiny`. However, in Case 3 where `vmin = 0.5` and `vmax = -0.5`, due to swapping `vmin` and `vmax`, the condition is met, which leads to incorrect modifications of the endpoints.

### Bug Fix Strategy:
To fix this bug, we need to ensure that the condition is modified to consider the absolute difference between `vmax` and `vmin`, so that the order of the values doesn't affect the behavior.

### Corrected Code:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmin), abs(vmax))

    if abs(vmax - vmin) <= maxabsvalue * tiny:
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

This corrected version of the function should now handle the edge cases correctly, preventing the errors encountered in the failing tests.