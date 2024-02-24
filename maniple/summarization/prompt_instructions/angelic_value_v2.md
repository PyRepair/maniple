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



{0}

{1}

## Summary:

[Your summary here.]