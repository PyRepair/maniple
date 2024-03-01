To fix the bug in the `_dict_arg` function, we need to ensure that the key-value pairs from the input dictionary are properly formatted in the `command` list without extra quotes. The issue arises from adding extra quotes around the values in the command list.

We can fix this bug by removing the extra quotes around the key-value pairs when adding them to the `command` list.

Here is the corrected version of the `_dict_arg` function:

```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

With this correction, the function should now properly format the key-value pairs without extra quotes, satisfying the expected input/output values for both cases stated above.