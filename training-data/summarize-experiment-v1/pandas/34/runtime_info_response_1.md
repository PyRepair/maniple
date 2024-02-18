The bug in the function is caused by the fact that the index used to check for odd or even positions is based on the reversed string. This means that for the original input, the function is actually applying the transformation based on the characters in their original positions, rather than in the reversed string as intended.

To fix this bug, we can simply reverse the string before applying the transformation. Here's the corrected function:

```python
def obscure_transform(text):
    text = text[::-1]  # Reverse the input string
    result = ""
    for i, char in enumerate(text):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this fix, the function correctly reverses the input string before applying the transformation, resulting in the expected output.