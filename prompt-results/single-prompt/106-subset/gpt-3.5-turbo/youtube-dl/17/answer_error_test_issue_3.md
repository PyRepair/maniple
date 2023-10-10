```python
def cli_bool_option(params, command_option, param, true_value='true', false_value='false', separator=None):
    param = params.get(param)
    if param is None:
        return []
    if separator:
        return [command_option + separator + (true_value if param else false_value)]
    if isinstance(param, bool):
        return [command_option, true_value if param else false_value]
    else:
        return []

```