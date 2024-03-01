#### Bug Analysis:
The bug occurs when handling form data for parameters of non-typing sequences such as Python lists, sets, and tuples. The error message indicates a 422 status code (validation error) instead of the expected 200 status code.

#### Error Locations:
1. The issue arises when trying to obtain the values for items inside the received form data.
2. Handling the validation errors and status codes incorrectly based on the conditionals.

#### Bug Cause:
The bug is caused by the function incorrectly handling non-typing sequences such as lists, sets, and tuples for form data parameters. It fails to properly extract values from the form data and handle validation errors leading to incorrect status codes.

#### Bug Fix Strategy:
1. Ensure that the values for non-typing sequence parameters are correctly retrieved from the form data.
2. Fix the handling of validation errors and status codes to match the expectations based on the successful data submission.

#### Corrected Version:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        for field in required_params:
            field_info = get_field_info(field)
            value = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            if value is None and field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                if (field.shape in sequence_shapes and lenient_issubclass(field.type_, list)):
                    field_value = value if value is not None else []
                    v_, errors_ = field.validate(field_value, values, loc=("body", field.alias))
                    if isinstance(errors_, ErrorWrapper):
                        errors.append(errors_)
                    elif isinstance(errors_, list):
                        errors.extend(errors_)
                    else:
                        values[field.name] = v_
                else:
                    v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                    if isinstance(errors_, ErrorWrapper):
                        errors.append(errors_)
                    elif isinstance(errors_, list):
                        errors.extend(errors_)
                    else:
                        values[field.name] = v_
    return values, errors

```

This corrected version should address the issues with handling non-typing sequence parameters and validation errors based on the test cases provided.