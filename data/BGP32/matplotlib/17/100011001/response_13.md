### Bug Explanation
The bug in the `nonsingular` function occurs when trying to calculate the `maxabsvalue`, leading to potential overflow issues. The error messages `RuntimeWarning: overflow encountered in scalar subtract` and `RuntimeWarning: overflow encountered in scalar absolute` indicate that the subtraction operation `vmax - vmin` and the absolute value calculation `abs(vmin)` or `abs(vmax)` respectively, face overflow problems due to the large input values, particularly in Case 4 with `vmin` as `-inf`.

### Bug Fix Strategy
To fix this bug, we need to restructure the calculation of `maxabsvalue` to prevent overflow issues when dealing with large input values. One approach is to first handle the infinite cases separately before calculating the maximum absolute value between `vmin` and `vmax`.

### Corrected Version
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return -expander, expander

    if vmax < vmin:
        vmin, vmax = vmax, vmin

    maxabsvalue = expander
    if vmax != vmin: 
        if abs(vmax) > abs(vmin):
            maxabsvalue = abs(vmax)
        else:
            maxabsvalue = abs(vmin)
        
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

    if increasing and vmax < vmin:
        vmin, vmax = vmax, vmin

    return vmin, vmax
```

This corrected version addresses the overflow issues by properly calculating `maxabsvalue` and handling the infinite cases. Additionally, it maintains the functionality of expanding the range if needed and swapping the endpoints based on the `increasing` parameter. After applying these changes, the function should pass the failing tests by avoiding overflow errors.