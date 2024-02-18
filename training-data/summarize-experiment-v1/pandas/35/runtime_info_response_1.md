The bug in the obscure_transform function lies in the enumeration of the reversed string. The function's logic correctly alternates between converting characters to upper and lower case, but it does so based on the index of the characters in the reversed string. This means that when the input string is reversed, the index of each character changes, causing the transformation to be applied incorrectly.

To fix this bug, we need to reverse the string before applying the enumeration, so that the transformation is based on the original index of the characters in the input string.

Here's the corrected code for the obscure_transform function:

```python
def obscure_transform(text):
    result = ""
    reversed_text = text[::-1]  # reverse the input string
    for i, char in enumerate(reversed_text):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this fix, the function correctly applies the transformation to the input string before returning the result.