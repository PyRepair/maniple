The bug in the `_dict_arg` function is caused by the formating of the command list. The values are being wrapped in additional quotes which are not required.

To fix the bug, we need to remove the extra quotes around the `{0}={1}` formatting in the list append operation.

Here is the corrected version of the function:

```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, "{0}={1}".format(prop, val)]
    return command
```

This corrected version removes the unnecessary quotes around the property-value pairs when adding them to the command list. It now correctly formats the command list as expected.