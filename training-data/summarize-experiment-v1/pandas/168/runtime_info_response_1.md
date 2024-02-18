The bug in the function is caused by the use of the `enumerate` function, which returns both the index and the value of each character in the reversed text. However, the bug is that the enumeration starts from 0, not from 1 which results in the incorrect application of the transformation rule.

To fix this bug, we can simply add 1 to the index `i` before checking if it is even or odd. This will correctly alternate between uppercasing and lowercasing the characters. 

Here is the corrected code:

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

With this correction, the function should now work as intended and passed the failing tests.