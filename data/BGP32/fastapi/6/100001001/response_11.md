### Bug Explanation
The bug in the `request_body_to_args` function arises from how it processes and validates the values from the `received_body` parameter. In the provided cases, the function fails to handle the situation where `received_body` contains multiple values for the same field. The function currently only considers the last value in such cases, leading to incorrect behavior and validation errors.

### Bug Fix Strategy
To fix the bug in the `request_body_to_args` function, we need to modify the logic that retrieves the values from `received_body` to handle cases where there are multiple values for a field properly. Instead of just considering the last value, we should handle all values for a field correctly based on the field type and requirements.

### Corrected Version of the Function
Here is a corrected version of the `request_body_to_args` function with the bug fixed:

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
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    if field.alias in received_body:
                        value = received_body.getlist(field.alias)
                    else:
                        value = received_body.get(field.alias)
                else:
                    value = received_body.get(field.alias)
            if value is None or (
                isinstance(field_info, params.Form)
                and field.required
                and value == ""
            ):
                if field.required:
                    if PYDANTIC_1:
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias))
                        )
                    else:
                        errors.append(
                            ErrorWrapper(
                                MissingError(),
                                loc=("body", field.alias),
                                config=BaseConfig,
                            )
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

In this corrected version, we correctly handle multiple values for the same field by checking and extracting them appropriately from `received_body`. This fix should address the bug and prevent validation errors when multiple values are present for a field.