### Bug Analysis
The bug in the `nonsingular` function lies in the conditional block where it checks if `vmax - vmin <= maxabsvalue * tiny`. This condition may lead to an overflow warning due to the subtraction operation on very large or small values.

1. In Case 2, when `vmin = -0.5` and `vmax = 1.5`, the `maxabsvalue` calculation incorrectly results in `1.5`. This issue arises from using the `abs` function on the raw values instead of their magnitudes.
   
2. In Case 3, the swapping logic fails as intended, but due to the error in `maxabsvalue` calculation, the condition where a range is too small to be expanded is not correctly identified.

### Bug Fix
To address the bugs:
- Correct the calculation of `maxabsvalue` by using the magnitude of the `vmin` and `vmax` values.
- Perform the `vmax - vmin` check with proper consideration for the magnitudes.

### Corrected Function

```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return -expander, expander
    
    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True
    
    maxabsvalue = max(abs(vmin), abs(vmax))  # Update to use magnitude
    
    if maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:
        vmin = -expander
        vmax = expander
    
    elif abs(vmax - vmin) <= maxabsvalue * tiny:  # Modified condition
        if vmax == 0 and vmin == 0:
            vmin = -expander
            vmax = expander
        else:
            vmin -= expander * maxabsvalue
            vmax += expander * maxabsvalue
    
    if swapped and not increasing:
        vmin, vmax = vmax, vmin
    return vmin, vmax
```

By fixing the calculation of `maxabsvalue` and adjusting the range expansion condition, the `nonsingular` function should now handle the input scenarios correctly and pass the failing tests.