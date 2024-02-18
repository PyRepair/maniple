The bug in the obscure_transform function lies in the enumeration of the reversed string. The function's implementation reverses the string first and then applies the transformation. However, the desired behavior is to apply the transformation while iterating through the original input string in reverse order.

To fix the bug, we need to reverse the string after applying the transformation to ensure that the characters are modified in the correct order. We can achieve this by reversing the input string before applying the transformation inside the for loop.

Here's the corrected implementation of the obscure_transform function:

```python
def obscure_transform(text):
    result = ""
    reversed_text = text[::-1]  # Reverse the input string
    for i, char in enumerate(reversed_text):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this fix, the function should now correctly apply the transformation to the input string in reverse order, producing the expected output.