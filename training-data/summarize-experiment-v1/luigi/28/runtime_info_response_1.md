The bug in the obscure_transform function lies in the enumeration of the reversed string. The function's logic correctly alternates between converting characters to uppercase and lowercase, but using enumerate with reversed does not yield the expected result. This is because the enumeration assigns indices to characters based on their original order, not their reversed order.

To fix this bug, we can simply reverse the string before the loop and then iterate over it without using enumerate. Here's the corrected code:

```python
def obscure_transform(text):
    reversed_text = text[::-1]  # Reverse the input string
    result = ""
    for i, char in enumerate(reversed_text):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this fix, the function should correctly apply the desired transformation to the input string and produce the expected output for all test cases.