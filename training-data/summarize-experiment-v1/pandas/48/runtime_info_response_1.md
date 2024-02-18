The bug in the obscure_transform function lies in the enumeration of the reversed string. The function's implementation reverses the string first and then applies the transformation. However, the desired behavior is to apply the transformation while iterating through the original input string in reverse order.

To fix the bug, we need to reverse the string after applying the transformation to ensure that the characters are modified in the correct order. We can achieve this by reversing the input string before entering the loop and then applying the transformation. Here's the corrected code:

```python
def obscure_transform(text):
    result = ""
    text = text[::-1]  # reverse the input string
    for i, char in enumerate(text):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this corrected implementation, the function should produce the expected output for both test cases.