The bug in the `request_body_to_args` function lies in the `value` assignment logic when dealing with sequence-shaped fields such as lists, sets, and tuples. The function incorrectly handles these fields and fails to extract the values properly from the `received_body`. This results in incorrect validation and parsing of the input data.

To fix this bug, we need to ensure that the function correctly processes sequence-shaped fields and extracts the values from the `received_body` based on the field's alias.

Here is the corrected version of the `request_body_to_args` function:

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

        if value is None:
            if field.required:
                if PYDANTIC_1:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))
            else:
                values[field.name] = deepcopy(field.default)
            continue

        if field.shape in sequence_shapes and isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
            if isinstance(value, list):
                awaitables = [item.read() for item in value]
                value = sequence_shape_to_type[field.shape](await asyncio.gather(*awaitables))
            else:
                value = await value.read()

        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_

    return values, errors
```

With the corrections made, this updated function now correctly handles sequence-shaped fields and extracts values from FormData based on the field's alias. This should allow the function to parse the input data correctly and pass the failing tests provided.