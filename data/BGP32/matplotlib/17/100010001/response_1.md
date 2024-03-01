### Analysis:
The error messages in both failing tests indicate that an overflow condition is encountered while performing certain arithmetic computations within the `nonsingular` function. Specifically, the warnings `RuntimeWarning: overflow encountered in scalar subtract` and `RuntimeWarning: overflow encountered in scalar absolute` are raised when trying to calculate the absolute or difference of `vmin` and `vmax`, which are values that can potentially lead to overflow.

### Bug Identification:
The issue lies in the following block of code:
```python
maxabsvalue = max(abs(vmin), abs(vmax))
if maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:
    vmin = -expander
    vmax = expander
```

The formula `(1e6 / tiny) * np.finfo(float).tiny` is used to determine if the maximum absolute value of `vmin` and `vmax` is below a certain threshold. However, the calculation itself can lead to overflow issues when dealing with very large values.

### Bug Cause:
The bug is caused by the use of a formula that can lead to overflow when calculating the threshold based on a large value `(1e6 / tiny) * np.finfo(float).tiny`.

### Fix Strategy:
1. To avoid overflow, we can simplify the logic and directly check the absolute values of `vmin` and `vmax` against a threshold, without performing calculations that might lead to overflow.
2. We can handle the cases where `vmin` and `vmax` are already small or zero without introducing unnecessary arithmetic operations.

### Corrected Version:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    # Handle case when vmin and vmax are already small or zero
    if abs(vmin) < 1e-6 or abs(vmax) < 1e-6 or vmax - vmin <= tiny:
        vmin = -expander
        vmax = expander
    else:
        # Handle the general case without potential overflow
        maxabsvalue = max(abs(vmin), abs(vmax))
        if maxabsvalue < 1e6 * tiny:
            vmin = -expander
            vmax = expander
        else:
            vmin -= expander * abs(vmin)
            vmax += expander * abs(vmax)

    if vmax < vmin and increasing:
        vmin, vmax = vmax, vmin

    return vmin, vmax
```

By simplifying the threshold calculation and handling the cases of small or zero values separately, we can ensure that the function `nonsingular` does not encounter overflow issues and provides the correct expanded and swapped endpoints.