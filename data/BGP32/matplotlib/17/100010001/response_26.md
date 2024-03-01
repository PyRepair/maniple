The bug in the `nonsingular` function arises from the calculation of `maxabsvalue`, which can lead to overflows and RuntimeWarnings when dealing with extreme values, as shown in the error messages.

### Bug Explanation:
1. The error message indicates a "RuntimeWarning: overflow encountered in scalar subtract" when the difference between `vmax` and `vmin` is calculated, which suggests that the values involved are too large to be handled properly.
2. Similarly, another error message shows a "RuntimeWarning: overflow encountered in scalar absolute" when trying to calculate the absolute value of `vmin` and `vmax`, indicating another overflow issue.

### Bug Fix Strategy:
To fix the bug and avoid these overflow issues, we can modify the calculation of `maxabsvalue` to ensure that the absolute difference of `vmax` and `vmin` is correctly handled, especially when dealing with very large values.

### Corrected Function:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):

    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmax - vmin), tiny*1e-5)  # Updated calculation for maxabsvalue

    if vmax - vmin <= maxabsvalue * tiny:
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

This revised version of the `nonsingular` function should now handle extreme cases with large values more robustly and prevent the overflow issues that were causing the RuntimeWarnings.