### Bug Analysis
1. The bug is related to how the function handles form data for non-typing sequences like lists, sets, and tuples.
2. The error message indicates a status code of 422 instead of the expected 200, which means there is an issue with the validation of the form data.
3. The buggy function processes form data for different sequence shapes but fails to handle it correctly, leading to validation errors.
4. The bug seems to be particularly related to the logic involving the shape of the field and how the values are extracted from the received form data. There are issues with how the form data is being parsed and validated.

### Bug Fix Strategy
1. Update the logic for handling sequence shapes in the form data.
2. Ensure that data for non-typing sequences like lists, sets, and tuples is correctly extracted and validated.
3. Check the conditionals that determine how values are retrieved from the form data and handle sequence shapes appropriately.

### Corrected Version of the Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if isinstance(received_body, FormData):
                    value = received_body.getlist(field.alias) if field.shape in sequence_shapes else received_body.get(field.alias)
            if value is None:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    continue
                else:
                    values[field.name] = deepcopy(field.default)
                    continue
            if (
                field.shape and isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types)
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

By correcting the extraction and validation logic for non-typing sequences in form data, the function should now handle lists, sets, and tuples correctly and pass the failing tests.