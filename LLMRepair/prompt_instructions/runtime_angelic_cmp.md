Your task is to assist a developer in analyzing runtime information of a program to identify a bug. You will receive the source code of the function suspected to contain the bug, along with the values it is supposed to produce. These values include the input parameters (with their values and types) and the expected output versus runtime output (with the values and types of relevant variables) at the function's return. Note that if an input parameter's value is not mentioned in the expected output, it is presumed unchanged. Your role is not to fix the bug but to summarize by following the example below.


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


## Example Runtime values and types of variables inside the buggy function

### Case 1
#### Runtime values and types of the input parameters of the buggy function
night, value: `8`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Runtime values and types of variables right before the buggy function's return
total_cost, value: `720`, type: `int`

### Case 2
#### Runtime values and types of the input parameters of the buggy function
night, value: `9`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Runtime values and types of variables right before the buggy function's return
total_cost, value: `810`, type: `int`

### Case 3
#### Runtime values and types of the input parameters of the buggy function
night, value: `7`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Runtime values and types of variables right before the buggy function's return
total_cost, value: `700`, type: `int`

### Case 4
#### Runtime values and types of the input parameters of the buggy function
night, value: `10`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Runtime values and types of variables right before the buggy function's return
total_cost, value: `900`, type: `int`


## Example summary:
Case 1: Given the input parameters `nights=8` and `rate_per_night=100`, the function should return `790`, but it returns incorrect output `720`. The reason why it fails is that the functions seems to apply the discount for all nights, not just the ones over 7. The expected output might be calculated by `7 * 100 + 1 * 100 * 0.9 = 790`.

Case2: Given the input parameters `nights=9` and `rate_per_night=100`, the function should return `880`, but it returns incorrect output `810`. The reason is the same as above. The expected output might be calculated by `7 * 100 + 2 * 100 * 0.9 = 880`.

Case3: Given the input parameters `nights=7` and `rate_per_night=100`, the function should return `700`, but it returns correct output `700`. This is the expected output.

Case4: Given the input parameters `nights=10` and `rate_per_night=100`, the function should return `970`, but it returns incorrect output `900`. The reason is the same as above. The expected output might be calculated by `7 * 100 + 3 * 100 * 0.9 = 970`.


{0}

{1}

## Summary:

[Your summary here.]