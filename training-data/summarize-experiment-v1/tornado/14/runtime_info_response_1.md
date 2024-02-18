The bug in the obscure_transform function lies in the enumeration of the reversed string. The function's logic correctly alternates between converting characters to upper and lowercase, but using enumerate with reversed does not yield the expected result. Instead of enumerating through the reversed string, changing the positions of the characters themselves, the function enumerates through the characters of the original string in reverse order. As a result, the even and odd positions are determined based on the original string, not the reversed one.

To fix this bug, the enumeration should be done on the reversed string itself, allowing the alternating case transformation to occur in the correct order. Here's the corrected function:

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

With this correction, the function should now produce the expected transformations on the input strings provided in the failing tests.