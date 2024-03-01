## Bug Explanation
The bug in the `_dict_arg` function lies in the way it handles creating the command list. Specifically, when adding key-value pairs from the input dictionary to the command list, it wraps the value in double quotes even though it should not be wrapped.

In Case 1, the function incorrectly appends the key-value pair '--conf', '"Prop=Value"' to the command list. The expected behavior should be to append '--conf', 'Prop=Value' without the double quotes around the `Value`.

In Case 2, a similar issue arises where the function appends '--conf', '"prop1=val1"' instead of '--conf', 'prop1=val1'.

## Fix Strategy
To fix this bug, we need to modify the way key-value pairs are inserted into the command list. Specifically, we should only wrap the key in double quotes, not the entire key-value pair. This will ensure that the command list is correctly formatted without unnecessary quotes around the values.

## Corrected Version
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

By modifying the line `command += [name, '"{0}={1}"'.format(prop, value)]` to `command += [name, '{0}={1}'.format(prop, value)]`, the bug is fixed. Now the key-value pairs will be added to the command list without any unnecessary quotes around the values.