### Bug Explanation
The bug in the `_dict_arg` function lies in the way the command list is constructed. Currently, the function is adding the key-value pairs with quotes around them, which is leading to incorrect formatting when the command list is used later on.

### Bug Fix Strategy
We need to modify the way the key-value pairs are added to the `command` list. Instead of having quotes around the key-value pairs, we should add them as separate elements without quotes.

### Corrected Function
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, prop + '=' + val]
    return command
```

By using the corrected function above, the key-value pairs will be added to the `command` list without quotes around them, aligning with the expected input/output values.