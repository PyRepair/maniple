### Bug Analysis
The bug seems to be related to how the function `_dict_arg` processes the dictionary values. It seems to be adding unnecessary quotes around the values when constructing the `command` list, leading to a mismatch in the expected and actual values.

### Bug Explanation
1. In the first case, the `value` parameter is a dictionary `{'Prop': 'Value'}`. When the function constructs the `command` list, it adds quotes around the value, resulting in `['--conf', '"Prop=Value"']` instead of `['--conf', 'Prop=Value']`.

2. In the second case, the `value` parameter is a dictionary `{'prop1': 'val1'}`. Similarly, the function adds quotes around the value, leading to `['--conf', '"prop1=val1"']` instead of `['--conf', 'prop1=val1']`.

### Bug Fix Strategy
To fix the bug, we need to modify the function `_dict_arg` to not add unnecessary quotes around the values when constructing the `command` list.

### Corrected Version
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():  # Renamed value to val to avoid variable name conflict
            command += [name, '{0}={1}'.format(prop, val)]  # Removed unnecessary quotes
    return command
``` 

The corrected version of the function should now properly construct the `command` list without adding unnecessary quotes around the values. This should align with the expected output values in both test cases provided.