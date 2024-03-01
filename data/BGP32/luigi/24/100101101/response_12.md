### Bug Analysis
The bug in the `_dict_arg` function stems from the way it constructs the command list. The function incorrectly adds quotation marks around the value pair, causing the test cases to fail when comparing the expected command list format.

### Bug Explanation
1. In Case 1, the function constructs the command list with `['--conf', '"Prop=Value"']` instead of the expected `['--conf', 'Prop=Value']`. This incorrect format of adding double quotation marks around the key-value pair leads to a mismatch with the expected output.
   
2. In Case 2, a similar issue occurs where the function constructs the command list as `['--conf', '"prop1=val1"']` instead of the expected format `['--conf', 'prop1=val1']`, resulting in test failure.

### Bug Fix Strategy
To fix the bug, we need to modify the `_dict_arg` function to correctly append key-value pairs without adding extra quotation marks around them. This can be achieved by changing the format in which the key-value pairs are added to the command list.

### Corrected Version of the Function
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

By making this modification, the corrected function will construct the command list in the expected format without unnecessary quotation marks, ensuring that the test cases pass successfully.