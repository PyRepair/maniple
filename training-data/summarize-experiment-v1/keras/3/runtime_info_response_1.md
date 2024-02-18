The bug in the obscure_transform function lies in the enumeration of the reversed string. The current implementation reverses the input string and then loops through the characters, converting every other character to uppercase or lowercase based on its position. However, the enumeration in Python starts from 0, so when the string is reversed, the positions of the characters are also reversed. To fix this bug, we need to reverse the string after the enumeration is done.

Here's the corrected code for the obscure_transform function:

```python
def obscure_transform(text):
    result = ""
    for i, char in enumerate(text):
        if i % 2 == 0:
            result += char.lower()
        else:
            result += char.upper()
    return result[::-1]
```

With this correction, the function will properly transform the input string according to the specified rules and return the correct result.