## Bug Explanation
The bug in the `request_body_to_args` function lies in how the function handles values from `received_body` when the `field.shape` is a sequence shape (1 for list, set, or tuple). The function incorrectly accesses the values from `received_body` using the `.get()` method, which leads to incorrect extraction of values and invalid comparisons. This causes the function to fail for scenarios involving non-typing sequences like lists, sets, and tuples.

## Bug Fix Strategy
1. Modify the logic for extracting values from `received_body` specifically for sequence shapes to handle lists, sets, and tuples correctly.
2. Update the code to correctly validate and process the extracted values based on the field type, shape, and requirements.

## The Corrected Version of the Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        field = required_params[0]
        embed = getattr(get_field_info(field), "embed", None)
        if len(required_params) == 1 and not embed:
            received_body = {field.alias: received_body}
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    if field.type_ == list:
                        value = received_body.getlist(field.alias)
                    elif field.type_ == set:
                        value = set(received_body.getlist(field.alias))
                    elif field.type_ == tuple:
                        value = tuple(received_body.getlist(field.alias))
                    else:
                        value = received_body.get(field.alias)
                else:
                    value = received_body.get(field.alias)
            if value is None or (value == "" and field.required) or (len(value) == 0 and field.required):
                if field.required:
                    if PYDANTIC_1:
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias))
                        )
                    else:  # pragma: nocover
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig)
                        )
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                value = await value.read()
            elif field.shape in sequence_shapes and isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
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

By updating the `value` extraction logic based on the field type and handling non-typing sequences correctly, the corrected function should now handle scenarios involving lists, sets, and tuples appropriately and pass the failing tests.