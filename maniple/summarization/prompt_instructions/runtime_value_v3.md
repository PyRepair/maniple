Your task is to analyze the runtime input/output values of a buggy function by following the provided example analysis format below.

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

## Runtime values and types of variables inside the buggy function

### Case 1
#### Runtime values and types of the input parameters of the buggy function
nights, value: `8`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Runtime values and types of variables right before the buggy function's return
total_cost, value: `720`, type: `int`

### Case 2
#### Runtime values and types of the input parameters of the buggy function
nights, value: `9`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Runtime values and types of variables right before the buggy function's return
total_cost, value: `810`, type: `int`

### Case 3
#### Runtime values and types of the input parameters of the buggy function
nights, value: `7`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Runtime values and types of variables right before the buggy function's return
total_cost, value: `700`, type: `int`

### Case 4
#### Runtime values and types of the input parameters of the buggy function
nights, value: `10`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Runtime values and types of variables right before the buggy function's return
result, value: `900`, type: `int`


## Example Analysis:
### Case 1
Given the input parameters `nights=8` and `rate_per_night=100`. The value of `nights` is greater than 7, the function calculate `8 * 100 * 0.9` and return `720`.

### Case2
Given the input parameters `nights=9` and `rate_per_night=100`. The value of `nights` is greater than 7, the function calculate `9 * 100 * 0.9` and return `810`.

### Case3
Given the input parameters `nights=7` and `rate_per_night=100`. The value of `nights` is equal to 7, the function calculate `7 * 100` and return `700`.

### Case4
Given the input parameters `nights=10` and `rate_per_night=100`. The value of `nights` is greater than 7, the function calculate `10 * 100 * 0.9` and return `900`.


Now it's your turn to analyze the runtime input/output values of the buggy function.

{0}

{1}
