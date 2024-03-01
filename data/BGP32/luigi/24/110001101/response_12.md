### Bug Explanation
The bug in the `_dict_arg` function lies in the way the key-value pairs are being formatted into strings before being added to the `command` list. The current implementation is using double quotes around the key-value pairs, which is incorrect. The correct format should not have double quotes around the key-value pairs.

### Bug Fix Strategy
To fix the bug, we need to remove the double quotes around the key-value pairs when constructing the command list inside the loop. This will ensure that the key-value pairs are formatted correctly.

### Corrected Version of the `_dict_arg` function
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
``` 

By making this change, the function will correctly format the key-value pairs without extra double quotes, satisfying the expected input/output values provided.