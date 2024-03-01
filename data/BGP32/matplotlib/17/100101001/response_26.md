### Bugs in the original function:

1. The condition for checking if either `vmin` or `vmax` is not finite is using `np.isfinite()` incorrectly. This leads to incorrect handling of infinity values.

2. The calculation of `maxabsvalue` is incorrect when setting the maximum absolute value.

3. The logic for adjusting `vmin` and `vmax` based on the interval size and tiny value is flawed.

### Bug Fixes:

1. Update the condition to check for infinite values using `np.isinf()` instead of `np.isfinite()`.

2. Correct the calculation of `maxabsvalue` to consider both `vmin` and `vmax`.

3. Improve the logic for adjusting `vmin` and `vmax` based on the interval size and tiny value.

### Corrected Function:

```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (np.isinf(vmin) or np.isinf(vmax)):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmin), abs(vmax))
    
    if maxabsvalue < (1e6 * tiny) * np.finfo(float).tiny:
        vmin = -expander
        vmax = expander

    elif (vmax - vmin) <= (maxabsvalue * tiny):
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

By applying these fixes, the function should now correctly handle infinite values, calculate `maxabsvalue` accurately, and adjust `vmin` and `vmax` appropriately based on the interval size and tiny value. This corrected version should pass the failing tests.