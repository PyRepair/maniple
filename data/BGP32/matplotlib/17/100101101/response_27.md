### Bug Explanation:
1. In Case 1 and Case 2, the variables `vmin` and `vmax` are expected to be floats, but the function is not handling the casting of these values properly, which leads to unexpected types in the return.
2. In Case 3, the swapping logic is not correctly handled when `vmin` is greater than `vmax`, resulting in an incorrect swap.
3. In Case 4, when the input values are infinite, the function does not return the expected values of `-expander` and `expander` as mentioned in the function definition.

### Bug Fix Strategy:
1. Ensure that the input values of `vmin` and `vmax` are correctly cast to floats within the function.
2. Correct the swapping logic to handle the case where `vmin` is greater than `vmax`.
3. Update the condition for handling infinite input values to return the correct values of `-expander` and `expander`.

### Corrected Version of the Function:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    vmin = float(vmin)
    vmax = float(vmax)

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

    if swapped and not increasing:
        vmin, vmax = vmax, vmin

    return vmin, vmax
```

By making these changes in the function, it should now pass the failing test cases and return the expected output values.