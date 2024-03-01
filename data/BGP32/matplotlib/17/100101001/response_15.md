The bug in the `nonsingular` function stems from incorrect handling of infinite values. When the input `vmin` or `vmax` is infinite, the function should return `-expander, expander` instead of directly returning those values.

To fix the bug, we need to modify the handling of infinite input values in the function. We can check if the input values are infinite at the beginning of the function and return the appropriate values.

Here is the corrected version of the `nonsingular` function:

```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):

    if np.isinf(vmin) or np.isinf(vmax):
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

With this correction, the function should now handle infinite values appropriately and pass the failing tests.