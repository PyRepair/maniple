### Bug Explanation
The bug in the `_dict_arg` function lies in the line where the command is being constructed inside the loop. The issue is that the values are being enclosed in double quotes unnecessarily, leading to the incorrect format of the command list.

### Bug Fix Strategy
To fix this bug, we need to remove the unnecessary double quotes when constructing the command list inside the loop. This way, the command list will correctly follow the expected format.

### Corrected Version
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '{0}={1}'.format(prop, val)]
    return command
``` 

The corrected version of the function correctly constructs the command list without unnecessary double quotes, ensuring that the command list follows the expected format.