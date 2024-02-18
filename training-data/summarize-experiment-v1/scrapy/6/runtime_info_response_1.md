The bug in the function is caused by the use of the `enumerate` function, which returns both the index and the value of each character in the reversed text. However, the bug is that the enumeration starts from 0, not from 1 which results in the incorrect application of the transformation to the characters.

To fix this bug, we need to adjust the starting index of the enumeration so that it starts from 1 instead of 0. This can be done by adding 1 to the index value before checking if it's even or odd.

Here's the corrected code:
```python
def obscure_transform(text):
    result = ""
    for i, char in enumerate(reversed(text)):
        if (i + 1) % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this fix, the function will correctly apply the transformation to the input string and produce the expected output.