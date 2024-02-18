The bug in the function is in the step where it alternates the case of the characters. The current implementation checks for the index being even or odd for the reversed string, but it should be checking for even or odd indices in the original string. To fix this, we need to reverse the text and then iterate through the original string to apply the case transformation.

Here's the fixed function:

```python
def obscure_transform(text):
    text_reversed = text[::-1]  # Reverse the input string
    result = ""
    for i, char in enumerate(text):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this fix, the function should now correctly apply the specified transformation to the input string, resulting in the expected output for both test cases.