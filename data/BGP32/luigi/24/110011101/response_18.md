## Bug Explanation
The bug in the `_dict_arg` function stems from the fact that the current implementation converts the property-value pair in the dictionary to a string with double-quotes around the value. This causes the values to be enclosed in double-quotes in the resulting command list, leading to a mismatch with the expected values in the test cases.

In the failing test cases:
- Case 1 expects the command to be `['--conf', 'Prop=Value']`, but the function returns `['--conf', '"Prop=Value"']`.
- Case 2 expects the command to be `['--conf', 'prop1=val1']`, but the function returns `['--conf', '"prop1=val1"']`.

The bug causes the value in the command list to be surrounded by double-quotes, which is not the expected behavior.

## Fixing the Bug
To fix the bug, we need to remove the double-quotes from around the value when constructing the command list. This can be achieved by modifying the `_dict_arg` function to directly append the property and value without any additional characters.

## Corrected Version of the Function
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

With this corrected implementation, the command list will contain property-value pairs without any extra characters, which should match the expected values in the failing test cases.