The bug in the function is caused by the fact that the index used to check for odd or even positions is based on the reversed string. This means that for the original input, the function is actually applying the transformation based on the characters in their original positions, rather than in the reversed string as intended.

To fix this bug, we can first reverse the input text, and then apply the transformation on the reversed string. This ensures that the transformation is based on the correct positions of characters in the reversed string. 

Here's the corrected code for the obscure_transform function:
```python
def obscure_transform(text):
    reversed_text = text[::-1] # Reverse the input text
    result = ""
    for i, char in enumerate(reversed_text): # Apply transformation on the reversed string
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this fix, the function should now correctly apply the transformation to the reversed input string, resulting in the expected output for the test cases.