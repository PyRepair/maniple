```python
def _dict_arg(self, name, value):
    command = []
    if value is not None and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '"{0}={1}"'.format(prop, val)]
    return command
```