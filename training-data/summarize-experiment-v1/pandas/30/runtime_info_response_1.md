The bug in the obscure_transform function lies in the enumeration of the reversed string. The current implementation reverses the input string and then loops through the characters, converting every other character to uppercase or lowercase. However, it's important to note that the enumeration of the reversed string starts from the last character (index 0) and goes towards the first character, which means that the even and odd positions are reversed as well.

To fix the bug, we need to reverse the string after applying the transformation. Additionally, the transformation should start from the first character of the reversed string to ensure that the correct characters are being converted to uppercase or lowercase.

Here's the corrected version of the obscure_transform function:

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

With this corrected implementation, the function should produce the expected output for the given test cases.