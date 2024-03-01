The bug in the `nonsingular` function seems to be related to how the interval expansion and swapping are handled. 

### Bug Explanation:
1. In Case 1, the `maxabsvalue` is calculated incorrectly as 1 when it should be 1 (the maximum absolute value between 0 and 1).
2. In Case 2, the `maxabsvalue` is calculated incorrectly as 1.5 when it should be 1.5 (the maximum absolute value between -0.5 and 1.5).
3. In Case 3, the swapping logic does not correct the values when vmin is greater than vmax, resulting in incorrect values at the function's return.
4. In Case 4, the function does not handle the cases where vmin or vmax are infinite correctly.

### Bug Fix Strategy:
1. Correct the calculation of `maxabsvalue` to consider the actual maximum absolute value between vmin and vmax.
2. Fix the swapping logic to correctly handle the case where vmin is greater than vmax.
3. Handle the cases where vmin or vmax are infinite by setting them to `-expander` and `expander` respectively.

### Corrected Version of the Function:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    if vmin > vmax and increasing:
        vmin, vmax = vmax, vmin

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

    return vmin, vmax
```

This corrected version addresses the identified issues and should now handle the interval expansion and swapping correctly for different input cases.