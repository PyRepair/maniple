### Bug Analysis:
1. The function `request_body_to_args` is responsible for converting received request body parameters into arguments.
2. The bug seems to be related to handling non-typing sequences like lists, sets, and tuples passed as form data.
3. In Case 1, the bug causes only the last value to be considered, leading to incorrect validation.
4. The bug arises from the logic where only the last value is extracted for the field when handling sequence shapes and FormData.
5. The current implementation does not correctly handle non-typing sequences when received as form data, which leads to validation errors.

### Bug Fix Strategy:
1. Update the logic when handling sequence shapes in form data to properly extract all values for fields with non-typing sequences.
2. Ensure that the values extracted from form data for non-typing sequences are passed correctly for validation, avoiding the current behavior where only the last value is considered.

### Updated Corrected Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value: Any = None
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.shape == 1:
                    value = received_body.getlist(field.alias)
                else:
                    value = [received_body.getlist(field.alias + str(i)) for i in range(field.shape)]
            else:
                value = received_body.get(field.alias)
        if (
            value is None
            or (isinstance(field_info, params.Form) and value == "")
            or (
                isinstance(field_info, params.Form)
                and field.shape in sequence_shapes
                and len(value) == 0
            )
        ):
            if field.required:
                if PYDANTIC_1:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
            continue
        if (
            isinstance(field_info, params.File)
            and lenient_issubclass(field.type_, bytes)
            and isinstance(value, UploadFile)
        ):
            value = await value.read()
        elif (
            field.shape in sequence_shapes
            and isinstance(field_info, params.File)
            and lenient_issubclass(field.type_, bytes)
            and all(isinstance(sub_val, UploadFile) for sub_val in value)
        ):
            awaitables = [sub_value.read() for sub_value in value]
            contents = await asyncio.gather(*awaitables)
            value = sequence_shape_to_type[field.shape](contents)
        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_
    return values, errors
```

The corrected function now correctly handles non-typing sequences passed as form data and extracts all values for validation. This update should address the issue and ensure that the tests pass as expected.