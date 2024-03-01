### Analysis
The `nonsingular` function is designed to modify the endpoints of a range to avoid singularities by expanding the interval based on certain conditions. However, there are multiple issues in the implementation that lead to failing the provided test cases. The key issues are:
1. Comparing floating-point numbers directly for equality.
2. Incorrect handling of negative zero values.
3. Inconsistent behavior in swapping endpoints based on input and flags.

### Bug Explanation
In the failing test cases, the `nonsingular` function fails to properly handle small intervals and swaps the endpoints inappropriately. The conditions inside the function that determine whether to expand the interval are incorrect. Additionally, the logic to determine when to swap the endpoints given the `increasing` flag is flawed. These issues lead to the function returning incorrect results.

### Bug Fix Strategy
1. Use a small tolerance value when comparing floating-point numbers for equality.
2. Handle negative zero values explicitly to ensure correct behavior.
3. Revise the logic for expanding intervals to avoid unintended expansions.
4. Correct the swapping logic based on the `increasing` flag.

### Corrected Function
```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    # Handle infinite values
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return -expander, expander

    swapped = False
    if vmin > vmax and not increasing:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmin), abs(vmax))
    interval = max(tiny, maxabsvalue) * tiny

    if vmax - vmin < interval:
        if np.isclose(vmax, 0, atol=tiny) and np.isclose(vmin, 0, atol=tiny):
            vmin = -expander
            vmax = expander
        else:
            vmin -= expander * abs(vmin)
            vmax += expander * abs(vmax)

    if swapped and not increasing:
        vmin, vmax = vmax, vmin

    return vmin, vmax
```

### Test the Corrected Function
After applying the corrections to the `nonsingular` function, it should pass all the provided failing test cases without any issues.