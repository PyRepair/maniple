The bug in the function is caused by the fact that the index used to check for odd or even positions is based on the reversed string. This means that for the original input, the function is actually applying the transformation based on the characters in their original positions, rather than in the reversed string.

To fix this bug, we need to reverse the text before entering the for loop and then apply the transformation based on the reversed string. Here's the corrected code:

```python
def obscure_transform(text):
    reversed_text = text[::-1]  # Reverse the input text
    result = ""
    for i, char in enumerate(reversed_text):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this fix, the function should correctly apply the transformation based on the reversed text and produce the expected output for both test cases.