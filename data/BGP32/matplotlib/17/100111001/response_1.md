Based on the provided information, the bug in the `nonsingular` function seems to be related to handling extreme values and numeric computations. The error messages suggest that there are overflow issues and incorrect absolute value calculations affecting the function's behavior.

### Bug Explanation:
1. For Case 2: The function fails to correctly handle the absolute value calculation due to the overwhelming of numeric precision.
2. For Case 3: The swapping of values when `vmin > vmax` is not done correctly, leading to incorrect behavior.
3. The conditions related to the `maxabsvalue` calculation and checking intervals for expansion are causing issues related to precision and overflow.

### Bug Fix Strategy:
1. Improve the handling of absolute value calculations to prevent overflow issues.
2. Correct the swapping logic when `vmin > vmax`.
3. Adjust the conditions for interval expansion to be more precise.

### Corrected Function:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return -expander, expander

    swapped = False
    if vmin > vmax:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmin), abs(vmax))
    if maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:
        vmin = -expander
        vmax = expander
    elif abs(vmax - vmin) <= maxabsvalue * tiny:
        total_expansion = expander * max(maxabsvalue, tiny)
        vmin -= total_expansion
        vmax += total_expansion

    if swapped and not increasing:
        vmin, vmax = vmax, vmin

    return vmin, vmax
```

After applying these fixes, the `nonsingular` function should behave correctly and pass the failing test cases provided.