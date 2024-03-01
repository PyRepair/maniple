### Analysis
1. The function `_dict_arg` is supposed to create a list of command arguments based on the input dictionary.
2. The bug seems to be related to how the function handles the dictionary values.
3. The error message indicates a discrepancy in how the `prop=value` pairs are formatted in the output list.
4. The bug is likely caused by including unnecessary quotes around the property value while constructing the command list.
   
### Fix Strategy
To fix the bug, we need to remove the unnecessary quotes around the property value when constructing the command list.

### Corrected Version
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
```