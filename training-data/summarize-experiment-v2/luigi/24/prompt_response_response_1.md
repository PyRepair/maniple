The issue with the `_dict_arg` function is that it is not properly formatting the key-value pairs when building the `command` list. The values should not be enclosed in double quotes, and the key-value pairs should be separated by an equal sign without any quotes.

To fix this issue, the `_dict_arg` function needs to be modified to format the key-value pairs correctly.

Here's the corrected code for the `_dict_arg` function:

```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

This corrected function should now properly format the key-value pairs without enclosing them in double quotes, which will resolve the issue with the failing tests.