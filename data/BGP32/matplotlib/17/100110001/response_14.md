### Analysis:
1. The `nonsingular` function is used in the `test_colorbar_int` test to generate `vmin` and `vmax` values.
2. The error occurs due to overflow in the calculation of `maxabsvalue` with large integer values passed to the function.
3. The error message indicates that overflow is encountered during the calculation of the absolute value of `vmin` or `vmax`.
4. To solve the issue, we need to handle the calculation of `maxabsvalue` in a way that avoids overflow when dealing with large integer values.

### Solution:
We can modify the calculation of `maxabsvalue` by first converting `vmin` and `vmax` to float before calculating the maximum absolute value. This will prevent overflow issues when dealing with large integers.

### Corrected Version:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    vmin = float(vmin)  # Convert to float
    vmax = float(vmax)  # Convert to float

    maxabsvalue = max(abs(vmin), abs(vmax))

    if maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:
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
    return vmin, vmax
```

With the updated code that converts `vmin` and `vmax` to float before calculating `maxabsvalue`, the function should now handle large integer values correctly without encountering overflow issues.