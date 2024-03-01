### Bug Explanation
The bug lies in the `_dict_arg` function where it incorrectly formats the dictionary values before adding them to the `command` list. The function is currently enclosing the property-value pairs in double quotes, leading to a mismatch with the expected values.

### Bug Fix Strategy
To fix the bug, we need to remove the unnecessary double quotes when formatting the property-value pairs. This will ensure that the command list contains the correctly formatted values.

### Corrected Version of the Function
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

After making this change, the function should now correctly format the property-value pairs without enclosing them in double quotes, matching the expected values.