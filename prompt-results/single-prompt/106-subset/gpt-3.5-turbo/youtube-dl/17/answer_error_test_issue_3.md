To fix the bug in the `cli_bool_option` function, we need to modify the code to handle cases where the `param` value is `None`. We can do this by adding a condition to check for `None` and returning an empty list if the value is `None`. Here's the fixed code:

```python
def cli_bool_option(params, command_option, param, true_value='true', false_value='false', separator=None):
    param = params.get(param)
    if param is None:
        return []
    assert isinstance(param, bool)
    if separator:
        return [command_option + separator + (true_value if param else false_value)]
    return [command_option, true_value if param else false_value]
```