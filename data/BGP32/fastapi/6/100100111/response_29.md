### Analysis:
1. The `request_body_to_args` function is designed to map received body data to the required parameters based on the specified fields.
2. The function deals with various scenarios, including checking for required fields, handling form data, file uploads, and validation.
3. The bug seems to be related to processing sequences in form data, leading to incorrect handling of list, set, and tuple types.
4. The failing tests indicate issues with processing list, set, and tuple parameters sent as form data.

### Bug Cause:
- The bug occurs when handling list, set, and tuple parameters sent as form data where the `received_body` data doesn't get processed correctly for these types, leading to validation errors and incorrect output.

### Bug Fix Strategy:
- Update the logic for handling sequences in the form data to properly extract and validate the list, set, and tuple values.
- Refactor the logic related to sequence shapes to identify and process all sequence types appropriately.

### Updated Function:
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
            field_value = []
            if received_body:
                if isinstance(received_body, FormData):
                    if field.shape in sequence_shapes:
                        field_value = received_body.getlist(field.alias)
                    else:
                        field_value = received_body.get(field.alias)
            if field_value is None or field_value == "":
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                    if isinstance(field_value, UploadFile):
                        field_value = await field_value.read()

                if field.shape in sequence_shapes:
                    if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                        field_value = [await sub_value.read() for sub_value in field_value]

                _, errors_ = field.validate(field_value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = _
    return values, errors
```

### Summary:
The updated `request_body_to_args` function now correctly handles sequences in form data and should address the reported issue while passing the provided failing test cases. Make sure to run additional tests to validate the fixed function's behavior in various scenarios.