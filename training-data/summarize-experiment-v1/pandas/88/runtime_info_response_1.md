The bug in the obscure_transform function lies in the enumeration of the reversed string. The function's implementation reverses the string first and then applies the transformation. However, the desired behavior is to apply the transformation while iterating through the original input string in reverse order.

To fix the bug, we need to reverse the string first and then iterate through it in reverse order to apply the transformation. Here's the corrected function:

```python
def obscure_transform(text):
    result = ""
    reversed_text = text[::-1]
    for i, char in enumerate(reversed_text):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this correction, the function will correctly apply the transformation to the input string in the intended order, resulting in the expected output for both test cases.