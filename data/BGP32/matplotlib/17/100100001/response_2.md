## Analysis:
The `nonsingular` function is designed to adjust the endpoints of a range to avoid singularities. The function handles cases where one or both endpoints are infinite or not finite, swaps the endpoints if necessary, expands the interval based on a threshold value, and makes adjustments if the interval is small.

The failing test `test_colorbar_int` is related to creating a color bar in matplotlib and checking if the `vmin` and `vmax` values of the image match the expected values (`clim`).

## Bugs:
1. The condition `swapped and not increasing` is not converting the swapped values back when the function was not intended to be increasing.
2. The adjustment logic inside the `elif` block where `vmin` and `vmax` are adjusted using `expander` does not handle cases where `vmax` or `vmin` is negative.

## Bug Fix Strategy:
1. Ensure that the swapping of `vmin` and `vmax` is correctly handled based on the `increasing` parameter.
2. Adjust the adjustment logic inside the `elif` block to properly handle negative `vmin` or `vmax`.

## Corrected Version:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        if increasing:
            vmin, vmax = vmax, vmin
            swapped = True
    else:
        if not increasing:
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
            if vmin < 0:
                vmin -= expander*abs(vmin)
            else:
                vmin -= expander*vmin

            if vmax < 0:
                vmax += expander*abs(vmax)
            else:
                vmax += expander*vmax

    return vmin, vmax
```

By correcting the issues mentioned above, the function `nonsingular` should now work correctly and pass the failing test.