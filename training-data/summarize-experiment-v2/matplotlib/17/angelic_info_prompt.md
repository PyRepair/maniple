You have been given the source code of a function that is currently failing its test cases.

Your mission involves analyzing each test case of expected input/output values step by step and compare it with the core logic of the function. Using this comparisons, formulate the reason for the discrepancy and summarise it.


# Expected value and type of variables during the failing test execution
Each case below includes input parameter value and type, and the expected value and type of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.

## Expected case 1
### Input parameter value and type
vmin, value: `0`, type: `int`

vmax, value: `1`, type: `int`

expander, value: `0.05`, type: `float`

tiny, value: `1e-15`, type: `float`

increasing, value: `True`, type: `bool`

### Expected value and type of variables right before the buggy function's return
swapped, expected value: `False`, type: `bool`

maxabsvalue, expected value: `1`, type: `int`

## Expected case 2
### Input parameter value and type
vmin, value: `-0.5`, type: `float`

vmax, value: `1.5`, type: `float`

expander, value: `0.05`, type: `float`

tiny, value: `1e-15`, type: `float`

increasing, value: `True`, type: `bool`

### Expected value and type of variables right before the buggy function's return
swapped, expected value: `False`, type: `bool`

maxabsvalue, expected value: `1.5`, type: `float`

## Expected case 3
### Input parameter value and type
vmin, value: `0.5`, type: `float`

vmax, value: `-0.5`, type: `float`

expander, value: `0.05`, type: `float`

tiny, value: `1e-15`, type: `float`

increasing, value: `True`, type: `bool`

### Expected value and type of variables right before the buggy function's return
vmin, expected value: `-0.5`, type: `float`

vmax, expected value: `0.5`, type: `float`

swapped, expected value: `True`, type: `bool`

maxabsvalue, expected value: `0.5`, type: `float`

## Expected case 4
### Input parameter value and type
vmin, value: `-inf`, type: `float`

vmax, value: `inf`, type: `float`

expander, value: `0.05`, type: `float`

tiny, value: `1e-15`, type: `float`

increasing, value: `True`, type: `bool`