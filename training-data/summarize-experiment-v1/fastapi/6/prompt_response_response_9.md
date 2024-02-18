The bug in the `request_body_to_args` function lies in the logic for handling `FormData` with multiple repeated keys. The function is not correctly handling repeated keys in `FormData` and is not populating the received body values correctly.

The cause of the bug is that the function does not appropriately handle repeated keys in `FormData`. When the `FormData` contains multiple repeated keys, the function does not group these values and assign them as a list to the same key before validation.

Here is the corrected code for the `request_body_to_args` function:

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
                    values[field.alias] = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
                    if value is None:
                        if field.required:
                            if PYDANTIC_1:
                                errors.append(
                                    ErrorWrapper(MissingError(), loc=("body", field.alias))
                                )
                            else:  # pragma: nocover
                                errors.append(
                                    ErrorWrapper(  # type: ignore
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

With this corrected code, the `request_body_to_args` function should now correctly handle repeated keys in `FormData`, group these values, and assign them as a list to the same key before validation. This fix addresses the issue posted in the GitHub repository related to supporting repeated key=value in form data.