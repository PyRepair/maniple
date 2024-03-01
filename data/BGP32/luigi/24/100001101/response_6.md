The bug in the `_dict_arg` function lies in the way the properties and values are added to the `command` list. The bug is caused by the unnecessary quotes around the property and value when creating the command string.

To fix the bug, we need to remove the quotes around `{0}={1}` in the `format` function. This will ensure that the property and value are added correctly to the command list without unnecessary quotes.

Here is the corrected version of the function:

```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

With this correction, the function should now correctly create the command list with properties and values without unnecessary quotes.