### Bug Analysis:
The bug lies in the logic of the `nonsingular` function in handling cases where either `vmin` or `vmax` is infinite. The current implementation does not correctly handle these cases causing the tests to fail.

### Bug Explanation:
- In Case 3, when `vmin = 0.5` and `vmax = -0.5`, the function correctly swaps the values due to `vmax < vmin`. However, the implementation fails to expand the endpoints causing the values to remain unchanged. Additionally, the `swapped` variable is set to `True` but not considered in the final return value.
- In Case 4, when `vmin = -inf` and `vmax = inf`, the function should return `(-expander, expander)`. However, the current check only handles finite values and does not account for infinite values.

### Bug Fix:
To fix the bug, we need to enhance the function to handle cases where `vmin` or `vmax` is infinite correctly. We should also ensure that when swapping the values, the `swapped` variable is correctly considered in the final return.

### Corrected Version of the Function:
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    swapped = False
    if vmax < vmin:
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

    if swapped and not increasing:
        vmin, vmax = vmax, vmin

    return vmin, vmax
``` 

With this corrected version, the function will correctly handle cases with infinite values or when values need to be swapped, ensuring the tests pass.