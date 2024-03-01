## Analysis:
1. The `nonsingular()` function takes two input parameters, `vmin` and `vmax`, and adjusts them to avoid singularities based on certain conditions.
2. The function has conditions to handle cases where the input parameters are not finite, where `vmax` is less than `vmin`, and where the interval is too small.
3. The bug in the function could be related to how it handles the adjustments in cases where `vmax` is less than `vmin`.
4. The failing test `test_colorbar_int()` creates an image plot with specified limits and checks if the normalization values match the input limits.
5. The failing test suggests that the normalization calculation within the `imshow()` function is not working as expected, potentially due to incorrect handling of `vmin` and `vmax` values.

## Bug Cause:
The bug in the `nonsingular()` function is caused by the incorrect adjustment of `vmin` and `vmax` when the condition `vmax < vmin` is met. The function should swap the values and set the `swapped` flag to `True`. However, the function is not correctly checking and adjusting the values when `vmax < vmin`.

## Fix Strategy:
To fix the bug, we need to ensure that the function correctly swaps `vmin` and `vmax` if `vmax < vmin` and sets the `swapped` flag accordingly. This way, the function will handle the cases where the input values need to be adjusted based on their relationship.

## Corrected Function:
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
            vmin -= expander*abs(vmin)
            vmax += expander*abs(vmax)

    if swapped and not increasing:
        vmin, vmax = vmax, vmin
    return vmin, vmax
```

By correctly swapping `vmin` and `vmax` when `vmax < vmin`, the corrected function should now handle the cases where the input values need adjustment to avoid singularities. This should ensure that the failing test `test_colorbar_int()` passes with the corrected function.