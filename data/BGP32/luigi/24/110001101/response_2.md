## Bug Explanation
The bug in the `_dict_arg` function arises from the way string formatting is done for the key-value pairs in the dictionary. The buggy function is incorrectly adding double quotes around the key-value pairs in the command list, resulting in an incorrect format.

## Bug Fix Strategy
To fix the bug, we need to remove the double quotes around the key-value pairs when adding them to the command list.

## Corrected Version of the Function

```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
``` 

With this corrected version of the function, the key-value pairs in the command list will be formatted correctly without unnecessary quotes.