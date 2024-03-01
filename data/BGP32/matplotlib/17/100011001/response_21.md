### Bug Explanation
The bug occurs due to potential overflow and incorrect handling of extreme input values within the `nonsingular` function. We encounter `RuntimeWarning: overflow encountered in scalar subtract` and `RuntimeWarning: overflow encountered in scalar absolute` errors when `maxabsvalue * tiny` or `abs(vmin)` and `abs(vmax)` are calculated, respectively. These errors are a result of the calculations leading to values outside the representable range for scalar data types.

### Bug Fix Strategy
To address the overflow issue and handle extreme input values correctly, we should revise the logic in the function to ensure that the calculations do not lead to such scenarios. It's important to consider extreme cases such as `inf`, `-inf`, and `0` for `vmin` and `vmax` and adjust the calculations accordingly to avoid overflows.

### Corrected Function
Here is the corrected version of the `nonsingular` function:

```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return -expander, expander

    swapped = False
    if increasing and vmin > vmax:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(np.abs(vmin), np.abs(vmax))
    if maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:
        vmin = -expander
        vmax = expander

    elif vmax - vmin <= maxabsvalue * tiny:
        if np.isclose(vmax, 0) and np.isclose(vmin, 0):
            vmin = -expander
            vmax = expander
        else:
            vmin -= expander * np.abs(vmin)
            vmax += expander * np.abs(vmax)

    if swapped and not increasing:
        vmin, vmax = vmax, vmin

    return vmin, vmax
```

By using `np.abs` instead of `abs`, handling `inf` or `-inf` explicitly, and using `np.isclose` for zero-checks, the function should now be able to handle extreme scenarios without running into overflow issues, passing the failing tests.