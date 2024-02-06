The function `request_body_to_args` takes in two parameters, `required_params` and `received_body`, and returns a tuple containing `values` and `errors`. The main logic of the function involves processing the `received_body` based on the `required_params` and populating the `values` dictionary and `errors` list accordingly.

The function iterates through the `required_params`. For each parameter, it retrieves the value from the `received_body` based on its `alias`. If the value is not found or does not meet the validation criteria, an error is appended to the `errors` list. Otherwise, the value is added to the `values` dictionary.

In the expected test cases, the function is expected to handle `FormData` input and populate `errors` and `values` based on the validation logic specified for each `required_param`. The function makes use of PYDANTIC_1 to determine the error type and form validation.

The key steps include:
1. Retrieving the value from `received_body` using the alias of each `required_param`.
2. Validating the retrieved value based on the type and required constraints.
3. Populating the `values` dictionary with the validated value or the default value if no error is encountered.
4. Appending errors to the `errors` list according to the validation results.

The function uses various condition checks and type validations to process the `received_body` and populate `values` and `errors` as expected.