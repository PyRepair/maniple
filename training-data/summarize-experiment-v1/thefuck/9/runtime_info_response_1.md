The bug in the obscure_transform function lies in the enumeration of the reversed string. The function's logic correctly alternates between converting characters to upper and lower case, but it does so based on the index of the characters in the reversed string. As a result, the original positions of the characters in the input string are not being properly reflected in the output.

To fix the bug, the function needs to reverse the input string before applying the character transformation. This ensures that the alternating uppercase and lowercase conversion is applied correctly based on the original positions of the characters.

Here's the corrected code:
```python
def obscure_transform(text):
    result = ""
    reversed_text = text[::-1]  # reverse the input string
    for i, char in enumerate(reversed_text):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```