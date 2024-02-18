The bug in the obscure_transform function lies in the enumeration of the reversed string. The function's logic correctly alternates between upper and lower case letters, but it using enumerate with reversed does not yield the expected result. To fix this bug, we should reverse the string first and then apply the indexing for the alternating upper and lower case transformation.

Here's the corrected code:
```python
def obscure_transform(text):
    reversed_text = text[::-1]  # Reverse the input text
    result = ""
    for i, char in enumerate(reversed_text):  # Enumerate the reversed text
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result
```

With this corrected code, the function will output the expected transformed string for the given input values.