### Issues Identified:
1. In Case 2 and Case 3, the code does not handle the scenario where the difference between `vmax` and `vmin` is very small but not exactly zero, causing potential errors when computing with very small values.
2. The way the code checks for finite values in the input is not correctly handled for negative infinity and positive infinity.
3. The logic for checking if `vmax < vmin` and swapping them works, but it is not considering the case where `vmin == vmax`.

### Solution:
1. Update the check for avoiding singularities to properly handle cases where the difference between `vmax` and `vmin` is very small but not exactly zero by comparing the absolute difference to a small threshold value.
2. Update the check for finite values in the input to also include checking for negative and positive infinity.
3. Adjust the logic for swapping `vmin` and `vmax` to also consider equality between them.

### Corrected Function
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return -expander, expander

    if vmin >= vmax:
        vmin, vmax = -expander, expander
        return vmin, vmax

    if np.isclose(vmax, vmin, atol=tiny):
        if np.isclose(vmax, 0, atol=tiny) and np.isclose(vmin, 0, atol=tiny):
            vmin, vmax = -expander, expander
        else:
            vmin -= expander * abs(vmin)
            vmax += expander * abs(vmax)

    maxabsvalue = max(abs(vmin), abs(vmax))
    if maxabsvalue < 1e6 * np.finfo(float).tiny / tiny:
        vmin = -expander
        vmax = expander

    if not increasing:
        if vmin > vmax:
            vmin, vmax = vmax, vmin

    return vmin, vmax
```

By updating the function with the above corrections, it should no longer encounter the errors mentioned in the failing test cases.