### Bug Explanation
The bug in the `_dict_arg` function arises from the string format used to create key-value pairs in the `command` list. The current implementation adds unnecessary double quotes around the key-value pairs, causing the test cases to fail as they expect a different format.

### Fix Strategy
To fix the bug, we need to remove the unnecessary double quotes around the key-value pairs when constructing the `command` list.

### Corrected Function
```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, "{0}={1}".format(prop, val)]
    return command
``` 

After applying this correction, the function should correctly construct key-value pairs in the expected format without unnecessary double quotes. This change will ensure that the test cases pass as they expect the key-value pairs without the extra quotes.