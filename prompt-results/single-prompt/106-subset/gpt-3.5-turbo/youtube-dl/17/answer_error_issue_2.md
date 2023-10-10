```python
def cli_bool_option(params, command_option, param, true_value='true', false_value='false', separator=None):
    param = params.get(param)
    if param is None:
        return []
    if isinstance(param, bool):  # Fix: Removed the assertion
        if separator:
            return [command_option + separator + (true_value if param else false_value)]
        return [command_option, true_value if param else false_value]
    else:
        raise ValueError("Parameter '{}' must be a boolean".format(param))
```
Explanation:
The bug in the code is due to the incorrect use of the `assert` statement. The `assert` statement is used for debugging purposes to verify that a certain condition is true. If the condition is false, it raises an `AssertionError` and terminates the program.

In this case, the `assert` statement is checking if the `param` is an instance of `bool`. However, this assertion is causing the program to fail because the `param` value is `None` instead of a boolean value.

To fix this bug, the `assert` statement can be removed, and instead, we can raise a `ValueError` if the `param` is not a boolean value.

Additionally, I added an `else` clause to handle the case when the `param` is not a boolean value. This will raise a `ValueError` with a descriptive error message to indicate that the parameter must be a boolean.

This fix ensures that the program no longer fails when the `param` value is `None`, and it correctly handles the case when a non-boolean value is provided.