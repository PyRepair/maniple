The issue in the `_dict_arg` function occurs when formatting the dictionary values into the command list. The current implementation does not correctly handle quoting values when appending them to the command list.

To address this issue, the function should ensure that the values from the dictionary are properly formatted and quoted when added to the command list.

Here's the corrected version of the `_dict_arg` function:

```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '"{0}={1}"'.format(prop, val)]
    return command
```

In the corrected version, the variable `val` is used instead of reusing the name `value` to avoid overwriting the input. Additionally, the value is properly quoted and formatted as per the requirements of the `spark-submit` command. This should resolve the issue with the incorrect formatting in the command list.