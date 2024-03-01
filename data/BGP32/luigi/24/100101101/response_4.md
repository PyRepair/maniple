### Bug Explanation
The bug in the `_dict_arg` function lies in the way the values are formatted and appended to the `command` list. The current implementation wraps the values in double quotes which leads to incorrect formatting when building the final command list.

### Bug Fix Strategy
To fix the bug, we need to remove the double quotes around the property values when formatting them before adding to the `command` list.

### Corrected Version of the Function
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

By removing the unnecessary double quotes in the formatting string, the corrected function will now correctly format and build the command list as expected. This should resolve the failing tests.