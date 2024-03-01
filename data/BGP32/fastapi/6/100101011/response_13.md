### Bug Analysis:
1. The `request_body_to_args` function processes required request parameters from the received body data. The bug appears to be related to handling sequence shapes (list, set, tuple) in the received body data.
2. The bug seems to stem from the way the function processes sequence shapes. It does not properly handle sequences of values for a single parameter, leading to validation errors and incorrect data processing.

### Bug Explanation:
1. In the failing test cases, the received body contains multiple values for a single parameter.
2. The function currently extracts these values sequentially, leading to validation errors due to incorrect handling of repeated keys in form data.
3. The conditionals for sequence shapes and checking for `FormData` handling are not appropriately managing sequence values.

### Bug Fix Strategy:
1. Adjust the logic for processing sequence shapes in the received body data to correctly handle repeated keys.
2. Modify the parsing of values for sequence shapes to ensure that all values are considered and processed when present.

### Bug-Fixed Version:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        field = required_params[0]
        for field in required_params:
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    if field.alias in received_body:
                        values[field.name] = received_body.getlist(field.alias)
                    else:
                        values[field.name] = []
                else:
                    value = received_body.get(field.alias)
                    if value is None or (isinstance(get_field_info(field), params.Form) and value == "") or (
                            isinstance(get_field_info(field), params.Form)
                            and field.shape in sequence_shapes
                            and len(value) == 0
                    ):
                        if field.required:
                            errors.append(
                                ErrorWrapper(MissingError(), loc=("body", field.alias))
                            )
                        else:
                            values[field.name] = deepcopy(field.default)
                    elif isinstance(get_field_info(field), params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                        value = await value.read()
                    elif field.shape in sequence_shapes and isinstance(get_field_info(field), params.File) and lenient_issubclass(
                        field.type_, bytes) and isinstance(value, sequence_types):
                        awaitables = [sub_value.read() for sub_value in value]
                        contents = await asyncio.gather(*awaitables)
                        values[field.name] = sequence_shape_to_type[field.shape](contents)
                    else:
                        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                        if isinstance(errors_, ErrorWrapper):
                            errors.append(errors_)
                        elif isinstance(errors_, list):
                            errors.extend(errors_)
                        else:
                            values[field.name] = v_
            else:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
    return values, errors
```

### Summary:
The bug was identified in the handling of sequence shapes in the received body data. By updating the logic within the function to properly manage repeated keys and sequence values, the corrected version should address the issue, pass the failing tests, and align with the feature request mentioned in the GitHub issue.