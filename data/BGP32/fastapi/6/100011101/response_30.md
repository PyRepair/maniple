The bug in the `request_body_to_args` function is related to how it handles non-typing sequences (list, set, tuple) in the received body. The function fails to correctly parse and process non-typing sequence values from the FormData. This results in validation errors and a status code of 422 instead of the expected status code of 200.

### Bug Explanation:
The core issue lies in the function's approach to handling non-typing sequences like list, set, and tuple. It expects the input to be in a specific format and fails to correctly parse the values when they are passed as part of FormData. The function wrongly processes the received values and encounters validation errors instead of correctly converting them to the expected sequence types.

### Fix Strategy:
To fix this bug, we need to update the function's logic to handle non-typing sequences properly when they are part of FormData. Specifically, we need to extract the sequence values from FormData correctly and convert them to the appropriate sequence types (list, set, tuple) as specified by the ModelField.

### Corrected Version of the Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value = None
        if received_body is not None:
            # Extract the value based on whether the field is a sequence
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                # Get list values for sequence shapes
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)

        if value is None:
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
            continue

        # Handle file type fields if present
        if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
            value = await value.read()

        # Validate the value against the field
        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_

    return values, errors
```

By updating the function with the corrected version, the function should now be able to properly handle non-typing sequences passed as part of FormData and convert them to the expected sequence types without encountering validation errors. The corrected version should pass the failing tests and return the expected output successfully.