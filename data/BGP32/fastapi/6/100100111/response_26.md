### Analysis:
1. The `request_body_to_args` function is responsible for converting received body data into arguments used for validation. It iterates over required parameters, extracts values from the received body, performs necessary transformations, and then validates the values.
2. The bug seems related to handling sequence shapes (`list`, `set`, `tuple`) in the received form data (`FormData`). The function fails to properly extract and handle multiple values for a single key in the form data, which is a key issue raised in the GitHub problem statement.
3. The bug causes the function to only consider the last value for a repeated key from the form data, leading to incorrect output and validation.
4. To fix the bug, we need to ensure that the function captures all values for a repeated key in the form data as a list or appropriate collection and passes it correctly for validation.
5. A corrected version of the function is provided below:

### Correction:
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
                if field.alias in received_body:
                    if field.shape == 1:
                        value = [received_body.get(field.alias)]
                    else:
                        value = received_body.getlist(field.alias)

            else:
                value = received_body.get(field.alias)

        if value is None or (isinstance(field_info, params.Form) and value == "") or (
            isinstance(field_info, params.Form)
            and field.shape in sequence_shapes
            and len(value) == 0
        ):
            if field.required:
                if PYDANTIC_1:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig)
                    )
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
            and isinstance(value, sequence_types)
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

This corrected version of the function now correctly handles multiple values for a single key in the form data by collecting them as a list before validation. This correction aligns with the expected behavior mentioned in the failing test cases and addresses the issue raised in the GitHub problem statement related to supporting repeated key=value pairs in form data.