The bug in the obscure_transform function lies in the enumeration of the reversed string. The current implementation reverses the input string and then loops through it while enumerating using the reversed() function. This causes the even and odd positions to be swapped due to the reversing. To fix this bug, we need to reverse the string after the enumeration to ensure that the correct transformation is applied.

```python
def obscure_transform(text):
    result = ""
    for i, char in enumerate(text):  # loop through the original string
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result[::-1]  # reverse the transformed string before returning
``` 

With this modification, the function should now correctly transform the input string according to the specified rules.