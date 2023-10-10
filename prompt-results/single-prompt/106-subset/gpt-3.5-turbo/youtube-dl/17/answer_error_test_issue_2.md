To fix this bug, I will modify the `cli_bool_option` function by checking if the value of `param` is `None` or `True` before asserting that it is of type `bool`. This will prevent the `AssertionError` from occurring when `param` is `None`.

Here is the fixed code:

```python
def cli_bool_option(params, command_option, param, true_value='true', false_value='false', separator=None):
    param = params.get(param)
    if param is None:
        return []
    assert param is True or param is False, "param must be boolean"
    if separator:
        return [command_option + separator + (true_value if param else false_value)]
    return [command_option, true_value if param else false_value]
```

Please let me know if you need any further assistance!