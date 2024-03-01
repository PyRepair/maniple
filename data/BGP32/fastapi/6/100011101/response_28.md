### Explanation:
1. The function `request_body_to_args` is designed to extract values from a request body based on the required parameters specified and return a dictionary of values and a list of errors.
2. The bug in the function seems to be related to how it handles requests with sequence shapes (list, set, tuple) when extracting values from the request body.
3. In the failing tests, the function fails to properly extract the values of sequences (list, set, tuple) from the FormData object provided.
4. The error message received indicates a status code of 422, which means there was a validation error in the request body parameters.
5. To fix the bug, the function needs to correctly handle the extraction of values for sequence shapes (list, set, tuple) from the FormData object and validate them accordingly.

### Bug Fix Strategy:
1. Update the logic that extracts and processes the values from the FormData object for sequence shapes.
2. Ensure that the extracted values for sequences are appropriately validated and returned without causing errors.
3. Handle the cases of list, set, and tuple parameter types correctly to align with expected behavior.

### Here is the corrected version of the function:
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
            if isinstance(received_body, FormData):
                value = received_body.getlist(field.alias) if field.shape in sequence_shapes else received_body.get(field.alias)
        if value is None or (isinstance(field_info, params.Form) and value == ""):
            if field.required:
                errors.append(
                    ErrorWrapper(MissingError(), loc=("body", field.alias))
                )
        else:
            if field.shape in sequence_shapes and isinstance(value, sequence_types):
                value = [await sub_value.read() for sub_value in value]
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

In the corrected version, the function now correctly handles the extraction of values for sequence shapes from the FormData object and ensures proper validation and processing to avoid errors.