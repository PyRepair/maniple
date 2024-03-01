### Bug Explanation:
The bug in the `nonsingular` function occurs when handling the case where the `maxabsvalue` is less than a certain threshold. The current implementation applies changes that are not aligned with the expected behavior, leading to incorrect output.

1. In Case 1, the function should return `(0.0, 1.0)` instead of `(0, 1)`.
2. In Case 2, the function should return `(0.0, 1.5)` instead of `(-0.5, 1.5)`.
3. In Case 3, the function should return `(-0.5, 0.5)` instead of `(0.5, -0.5)`.

### Bug Fix Strategy:
1. Adjust the logic inside the `nonsingular` function to correctly handle cases where `maxabsvalue` is less than the specified threshold.
2. Ensure that the function swaps `vmin` and `vmax` if `vmin` is greater than `vmax` and the `increasing` flag is set to `True`.

### Corrected Code:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    swapped = False
    if vmin > vmax and increasing:
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
    return float(vmin), float(vmax)
```