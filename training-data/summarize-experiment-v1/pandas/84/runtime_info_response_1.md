The bug in the function is caused by the use of the `enumerate` function, which returns both the index and the value of each character in the reversed text. However, the bug is that the enumeration starts from 0, not from 1, which leads to incorrect uppercase/lowercase conversion.

To fix this bug, we can simply adjust the enumeration to start from 1 instead of 0 by adding 1 to the index before checking if it's even or odd. The corrected function code is as follows:

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

With this fix, the function should now produce the correct output for the given test cases.