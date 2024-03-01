### Bug Analysis:
The bug arises due to potential overflow issues when performing operations in the `nonsingular` function. The error messages indicate that either an overflow occurs during scalar subtraction or when taking the absolute value of a scalar.

1. In the first case, when `vmin=0` and `vmax=1`, the calculation for `vmax - vmin` results in an overflow warning during scalar subtraction.
   
2. In the second case, `vmin=-0.5` and `vmax=1.5`, the calculation for `maxabsvalue = max(abs(vmin), abs(vmax))` results in an overflow warning when taking the absolute value of `vmax`.

3. In the third case, `vmin=0.5` and `vmax=-0.5`, the values of `vmin` and `vmax` are being swapped, resulting in `vmin=-0.5` and `vmax=0.5`. This highlights the need to handle swapped values correctly to avoid incorrect operations.

4. In the fourth case, when `vmin` and `vmax` are infinite, the function currently doesn't return the expected values for this scenario.

### Bug Fix Strategy:
To resolve the issue:
1. Address potential overflow warnings during scalar arithmetic operations by properly handling the calculations.
2. Ensure that absolute values are taken correctly without causing overflows or incorrect results.
3. Handle the case where one or both inputs are infinite to return appropriate values.

### Corrected Function:
```python
import numpy as np

def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if not np.isfinite(vmin) or not np.isfinite(vmax):
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
            vmin -= expander * abs(vmin)
            vmax += expander * abs(vmax)

    if not increasing and swapped:
        vmin, vmax = vmax, vmin

    return vmin, vmax
```

By correcting the arithmetic operations and handling the edge cases more effectively in the `nonsingular` function, the overflow issues and incorrect behaviors identified in the failing tests should be resolved.