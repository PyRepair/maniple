The bug in the function is caused by the fact that the index used to check for odd or even positions is based on the reversed string. This means that for the original input, the function is actually applying the transformation based on the characters in their original positions, rather than in the reversed string.

To fix this bug, the function should reverse the text first and then apply the transformation based on the reversed string. This can be done by first reversing the input string and then iterating over it to apply the transformation. 

Here is the corrected code for the function:

```python
def obscure_transform(text):
    reversed_text = text[::-1]  # reverse the input text
    result = ""
    for i, char in enumerate(reversed_text):  # iterate over the reversed text
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this correction, the function will correctly reverse the input string before applying the transformation, resulting in the expected output for the given test cases.