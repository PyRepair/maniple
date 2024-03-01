### Bug Analysis:
The bug in the `nonsingular` function originates from the calculation involving `maxabsvalue` and the comparison with `(1e6 / tiny) * np.finfo(float).tiny`. This leads to potential overflow issues and incorrect calculations, causing the failing tests.

1. In Case 1, the `maxabsvalue` calculation can result in an incorrect type conversion, causing issues with further calculations.
2. In Case 2, the `maxabsvalue` calculation does not handle floating-point values properly.
3. In Case 3, the swapping logic for `vmin` and `vmax` may not work correctly due to the condition check.
4. In Case 4, handling infinite values for `vmin` and `vmax` is not properly implemented, leading to incorrect return values.
5. In Case 5 and Case 7, the calculations involving `maxabsvalue` can lead to overflow issues.

### Bug Fix Strategy:
1. Ensure type consistency in calculations to prevent type conversions causing issues with floating-point values.
2. Handle special cases like infinite values for `vmin` and `vmax` to return correct values.
3. Improve the logic for determining when to expand the interval based on the tiny threshold to avoid overflow issues.

### Corrected Function:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    swapped = False
    if increasing and vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmin), abs(vmax))
    lower_bound = 1e6 * np.finfo(float).tiny / tiny
    if maxabsvalue < lower_bound:
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
    return np.float64(vmin), np.float64(vmax)
```

By making the above adjustments, the corrected function should now handle the input values correctly and pass the failing tests.