### Cause of the bug:
The bug arises from the incorrect formatting of the command list in the `_dict_arg` function. The function concatenates the name and value inside double quotes, resulting in unnecessary quotes in the final command list.

### Strategy for fixing the bug:
To fix the bug, we need to remove the unnecessary double quotes around the property-value pair when constructing the command list.

### Corrected version of the function:
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, "{0}={1}".format(prop, val)]
    return command
```