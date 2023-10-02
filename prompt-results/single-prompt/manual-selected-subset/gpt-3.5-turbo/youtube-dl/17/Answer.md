Sure, I can help you with that. It seems like the issue is with the line that checks the type of the parameter and the subsequent logic. To fix this, you can modify the code as follows:

    def cli_bool_option(params, command_option, param, true_value='true', false_value='false', separator=None):
        param = params.get(param)
        if param is None:
            return []  # Return empty list if param is None

        assert isinstance(param, bool)
        if separator:
            return [command_option + separator + (true_value if param else false_value)]
        return [command_option, true_value if param else false_value]

Here's what I changed:

Added a check for param is None at the beginning of the function. If the param is None, we return an empty list directly, as per your requirement.
Moved the assert isinstance(param, bool) check below the param is None check. This ensures that the assertion is only checked if param is not None.
The rest of the code remains the same, and the existing logic for creating the list is retained.

This change should fix the issue you were facing while still preserving the existing behavior for other cases.