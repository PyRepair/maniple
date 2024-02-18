The bug in the obscure_transform function lies in the enumeration of the reversed string. The function's logic correctly alternates between uppercasing and lowercasing characters using the enumerate() function, but it is enumerating the characters from the reversed string, which results in an incorrect transformation.

To fix this bug, we need to modify the enumeration process to iterate through the original string instead of the reversed string. We can achieve this by reversing the string first and then applying the enumeration to it. Here's the corrected code:

```python
def obscure_transform(text):
    result = ""
    for i, char in enumerate(reversed(text)):
        if i % 2 == 0:
            result += char.lower()
        else:
            result += char.upper()
    return result
```

With this change, the function should now correctly apply the case transformation to every other character in the original string and return the expected outputs for the given test cases.