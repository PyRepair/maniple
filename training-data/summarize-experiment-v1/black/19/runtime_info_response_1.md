The bug in the obscure_transform function lies in the enumeration of the reversed string. The function's implementation reverses the string first, and then applies the case modification using the enumerate() function. However, this results in modifying the case of characters in the original position rather than in the reversed position as intended.

To fix this bug, the enumeration process should be done on the original string before reversing it. This way, the case modification will be applied correctly based on the reversed order of characters.

Here's the corrected code:

```python
def obscure_transform(text):
    result = ""
    for i, char in enumerate(text[::-1]):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this correction, the function should now produce the expected output for the given test cases.