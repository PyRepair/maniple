The bug in the provided `nonsingular` function is in the calculation of `maxabsvalue`. The calculation is based on the maximum absolute value between `vmin` and `vmax`, and it should refer to the absolute values of the input numbers, not their original values.

The `maxabsvalue` should be recalculated to fix the bug. We should calculate the maximum absolute value between the absolute `vmin` and `vmax`, not the original values.

Here is the corrected version of the `nonsingular` function:

```python
import numpy as np

def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmin), abs(vmax))  # Calculate the maximum absolute value correctly

    if maxabsvalue < 1e6 * tiny * np.finfo(float).tiny:
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

This corrected version ensures that the `maxabsvalue` is calculated based on the absolute values of `vmin` and `vmax`. It should now satisfy all the expected test cases given.