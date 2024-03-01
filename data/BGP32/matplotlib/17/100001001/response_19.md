The bug in the `nonsingular` function stems from the calculation and conditions applied to expand and modify the endpoints of the range to avoid singularities. 

### Explanation of the bug:
1. In Case 1, when `vmin = 0` and `vmax = 1`, the initial `maxabsvalue` is calculated incorrectly as `1` instead of the correct maximum value `1` between `0` and `1`. This results in the condition `maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny` evaluating to False, which leads to the incorrect expansion of the endpoints leading to potential singularities.

2. In Case 2, when `vmin = -0.5` and `vmax = 1.5`, the `maxabsvalue` is calculated as `1.5`, which is correct. However, the condition to expand the endpoints is intended to be `(vmax - vmin) <= maxabsvalue * tiny`, but it's currently written as `vmax - vmin <= maxabsvalue * tiny` which can lead to an incorrect expansion.

3. In Case 3, when `vmin = 0.5` and `vmax = -0.5`, the endpoint swapping logic is correct, but the subsequent expansion based on the conditions is not properly handling the swapped case.

4. In Case 4, when one of the values is infinite, the current logic doesn't handle it properly, leading to an incorrect expansion strategy.

### Strategy to fix the bug:
1. Calculate the `maxabsvalue` correctly as the maximum absolute value between `vmin` and `vmax`.
2. Adjust the conditions for expanding the endpoints to ensure that singularities are avoided effectively, especially focusing on cases where the values are near zero or infinite.

### Corrected version of the `nonsingular` function:

```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)) or (vmin == vmax == 0) or (max(abs(vmin), abs(vmax)) < tiny):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmin), abs(vmax))
    if maxabsvalue < np.finfo(float).tiny:
        vmin = -expander
        vmax = expander
    elif (vmax - vmin) <= maxabsvalue * tiny:
        vmin -= expander * abs(vmin)
        vmax += expander * abs(vmax)

    if swapped and not increasing:
        vmin, vmax = vmax, vmin

    return vmin, vmax
```

This corrected version addresses the issues identified in each case and should now correctly handle the expansion and modification of endpoints to avoid singularities.