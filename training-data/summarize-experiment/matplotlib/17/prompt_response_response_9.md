The function `nonsingular` is encountering an overflow warning when computing the maximum absolute value of `vmin` and `vmax` due to the combined use of `max` and `abs` functions on potentially large numbers. The current code for calculating `maxabsvalue` is:

```python
maxabsvalue = max(abs(vmin), abs(vmax))
```

To address this issue, we can swap the positions of `max` and `abs` to first find the maximum of `vmin` and `vmax` and then apply the absolute function. This will prevent the overflow warning.

The revised code for calculating `maxabsvalue` is:

```python
maxabsvalue = abs(max(vmin, vmax))
```

After making this change, the function should compute `maxabsvalue` without encountering an overflow warning.

Here is the corrected version of the `nonsingular` function:

```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = abs(max(vmin, vmax))
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

    if swapped and not increasing:
        vmin, vmax = vmax, vmin
    return vmin, vmax
```

With this revised code, overflow warnings should no longer occur when computing `maxabsvalue`. This corrected function can be used as a drop-in replacement for the buggy version of the function.