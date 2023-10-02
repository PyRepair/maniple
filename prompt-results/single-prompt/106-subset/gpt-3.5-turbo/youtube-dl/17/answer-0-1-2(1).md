To fix the bug, we need to handle the case where the `param` value is `None` separately before checking its type. We can modify the code to return an empty list if `param` is `None`, ensuring that the assertion error is not raised in such cases.

Here's the fixed code:

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