```python
def _dict_arg(self, name, value):
    command = []
    if value and isinstance(value, dict):
        for prop, val in value.items():  # change variable name 'value' to 'val' to avoid confusion
            command += [name, '"{0}={1}"'.format(prop, val)]  # wrap prop and val in quotes
    return command
```