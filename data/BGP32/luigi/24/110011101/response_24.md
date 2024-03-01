### Problem Identification
The issue stems from the `_dict_arg` function where it incorrectly handles dictionary values by adding unnecessary quotes around property values. This results in a mismatch when comparing the expected output with the actual output, causing the test to fail.

### Bug Cause
The bug arises from the function adding double quotes around property values when constructing the command list. This behavior is not in alignment with the expected output where the values should be added without quotes.

### Solution Strategy
To fix this bug, we need to remove the unnecessary quotes around property values when constructing the command list. This can be achieved by directly appending the property and its value without quoting.

### Corrected Version
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, prop_value in value.items():
            command += [name, '{0}={1}'.format(prop, prop_value)]
    return command
``` 

By making this change, the function will correctly construct the command list without adding unnecessary quotes around property values, resolving the comparison mismatches and passing the failing tests.