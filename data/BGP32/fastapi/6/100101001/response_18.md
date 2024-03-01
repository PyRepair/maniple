The bug in the `request_body_to_args` function lies in how it handles non-typing sequences like lists, sets, and tuples when processing the received body data. The function incorrectly assumes that the value of a non-typing sequence will be directly available under the alias key in the received body. This assumption leads to validation errors and incorrect processing of the received data.

To fix the bug, we need to update the logic in the function to handle non-typing sequences correctly. We should iterate over the received values for non-typing sequence fields and process them accordingly.

Here is a corrected version of the `request_body_to_args` function:

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
                values[field.name] = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
                if (
                    value is None
                    or (isinstance(get_field_info(field), params.Form) and value == "")
                    or (
                        isinstance(get_field_info(field), params.Form)
                        and field.shape in sequence_shapes
                        and len(value) == 0
                    )
                ):
                    if field.required:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:
                        values[field.name] = deepcopy(field.default)
                    continue
                if (
                    isinstance(get_field_info(field), params.File)
                    and lenient_issubclass(field.type_, bytes)
                    and isinstance(value, UploadFile)
                ):
                    value = await value.read()
                elif (
                    field.shape in sequence_shapes
                    and isinstance(get_field_info(field), params.File)
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

This corrected version handles non-typing sequence fields correctly, reducing the chances of validation errors and ensuring that the received data is processed accurately.

After applying the fix, the function should be able to pass the failing tests provided.