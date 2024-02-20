## Bug Cause

The bug seems to be caused by the incorrect way the command list is being generated within the `_dict_arg` function. The function is supposed to create a command list based on the key-value pairs in the input dictionary, but it is currently not producing the expected output.

The issue seems to be in the line:
```python
command += [name, '"{0}={1}"'.format(prop, value)]
```
This line concatenates the name and formatted key-value pair as a string within double quotes, which is not the desired format and is causing the current bug.

## Approach to Fix the Bug

To fix the bug, the line creating the command list needs to be modified such that it correctly formats the key-value pairs in the expected format without unnecessary double quotes.

The corrected format should be:
```python
command += [name, "{0}={1}".format(prop, value)]
```

This will ensure that the key-value pairs are concatenated in the correct format and the command list is generated as expected.

## The corrected code

Here is the corrected version of the `_dict_arg` function:

```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, "{0}={1}".format(prop, val)]
    return command
```