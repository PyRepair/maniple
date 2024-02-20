Your task is to summarize the expected input and output values of a buggy function, following the example provided below.

## Example source code of the buggy function
```python
def calculate_total_cost(nights, rate_per_night):
    discount = 0.1  # 10% discount for stays longer than 7 nights
    if nights > 7:
        total_cost = nights * rate_per_night * (1 - discount)
    else:
        total_cost = nights * rate_per_night
    return total_cost
```

## Example expected value and type of variables during the failing test execution

### Expected case 1
#### Input parameter value and type
nights, value: `8`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `790`, type: `int`

### Expected case 2
#### Input parameter value and type
nights, value: `9`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `880`, type: `int`

### Expected Case 3
#### Input parameter value and type
nights, value: `7`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `700`, type: `int`

### Exptected Case 4
#### Input parameter value and type
nights, value: `10`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `970`, type: `int`


## Example summary:
Case 1: Given the input parameters `nights=8` and `rate_per_night=100`, the function should return `790`. This might be calculated by `7 * 100 + 100 * 0.9 = 790`.

Case2: Given the input parameters `nights=9` and `rate_per_night=100`, the function should return `880`. This might be calculated by `7 * 100 + 2 * 100 * 0.9 = 880`.

Case3: Given the input parameters `nights=7` and `rate_per_night=100`, the function should return `700`. This might be calculated by `7 * 100 = 700`.

Case4: Given the input parameters `nights=10` and `rate_per_night=100`, the function should return `970`. This might be calculated by `7 * 100 + 3 * 100 * 0.9 = 970`.



## The source code of the buggy function

```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    """
    Modify the endpoints of a range as needed to avoid singularities.

    Parameters
    ----------
    vmin, vmax : float
        The initial endpoints.
    expander : float, default: 0.001
        Fractional amount by which *vmin* and *vmax* are expanded if
        the original interval is too small, based on *tiny*.
    tiny : float, default: 1e-15
        Threshold for the ratio of the interval to the maximum absolute
        value of its endpoints.  If the interval is smaller than
        this, it will be expanded.  This value should be around
        1e-15 or larger; otherwise the interval will be approaching
        the double precision resolution limit.
    increasing : bool, default: True
        If True, swap *vmin*, *vmax* if *vmin* > *vmax*.

    Returns
    -------
    vmin, vmax : float
        Endpoints, expanded and/or swapped if necessary.
        If either input is inf or NaN, or if both inputs are 0 or very
        close to zero, it returns -*expander*, *expander*.
    """

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
            vmin -= expander*abs(vmin)
            vmax += expander*abs(vmax)

    if swapped and not increasing:
        vmin, vmax = vmax, vmin
    return vmin, vmax

```

## Expected values and types of variables during the failing test execution
Each case below includes input parameter values and types, and the expected values and types of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.

### Expected case 1
#### The values and types of buggy function's parameters
vmin, value: `0`, type: `int`

vmax, value: `1`, type: `int`

expander, value: `0.05`, type: `float`

tiny, value: `1e-15`, type: `float`

increasing, value: `True`, type: `bool`

#### Expected values and types of variables right before the buggy function's return
swapped, expected value: `False`, type: `bool`

maxabsvalue, expected value: `1`, type: `int`

### Expected case 2
#### The values and types of buggy function's parameters
vmin, value: `-0.5`, type: `float`

vmax, value: `1.5`, type: `float`

expander, value: `0.05`, type: `float`

tiny, value: `1e-15`, type: `float`

increasing, value: `True`, type: `bool`

#### Expected values and types of variables right before the buggy function's return
swapped, expected value: `False`, type: `bool`

maxabsvalue, expected value: `1.5`, type: `float`

### Expected case 3
#### The values and types of buggy function's parameters
vmin, value: `0.5`, type: `float`

vmax, value: `-0.5`, type: `float`

expander, value: `0.05`, type: `float`

tiny, value: `1e-15`, type: `float`

increasing, value: `True`, type: `bool`

#### Expected values and types of variables right before the buggy function's return
vmin, expected value: `-0.5`, type: `float`

vmax, expected value: `0.5`, type: `float`

swapped, expected value: `True`, type: `bool`

maxabsvalue, expected value: `0.5`, type: `float`

### Expected case 4
#### The values and types of buggy function's parameters
vmin, value: `-inf`, type: `float`

vmax, value: `inf`, type: `float`

expander, value: `0.05`, type: `float`

tiny, value: `1e-15`, type: `float`

increasing, value: `True`, type: `bool`

## Summary:

[Your summary here.]