The issue in the `_dict_arg` function is that it is incorrectly adding extra quotes around the property and value when forming the command. This leads to a mismatch in the expected and actual values during the test comparisons.

To fix this bug, we need to remove the extra quotes added around the property and value when constructing the command list.

Here is the corrected version of the `_dict_arg` function:

```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```

With this correction, the function should now correctly form the command list without unnecessary quotes. This fix should make the failing tests pass as the actual values match the expected values without any additional characters.