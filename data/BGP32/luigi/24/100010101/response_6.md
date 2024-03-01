### Bug Explanation:
The function `_dict_arg` is not handling the dictionary values correctly. It is adding extra quotes around the property values before appending them to the command list. This leads to discrepancies in the final command list when comparing it with the expected values from the test cases.

### Bug Fix Strategy:
To fix the bug, we need to remove the extra quotes around the property values before appending them to the command list. This can be achieved by directly formatting the string without additional quoting.

### Corrected Version of the Function:
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

By making this change, the corrected function should now properly format the command list without adding unnecessary quotes around the values, passing the failing tests.