### Analysis:
1. The function `request_body_to_args` is supposed to convert the received body data into arguments based on the required parameters list.
2. The failing tests are related to sending data as form data with repeated keys, and the function is not handling them correctly.
3. The error messages indicate that the response status code is 422 (Unprocessable Entity) instead of the expected 200 (OK).
4. The issue on GitHub suggests that FastAPI should handle repeated keys in form data correctly.

### Bug:
The bug in the function `request_body_to_args` lies in how it processes repeated keys in form data. It only selects the last key=value pair and does not handle multiple values for the same key as a list.

### Fix Strategy:
1. Check for cases where multiple values exist for the same key in form data.
2. Modify the function to handle such cases by storing multiple values for a key as a list.

### Corrected Version:
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
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
                    # Handle multiple values for the same key
                    if field.shape not in sequence_shapes and isinstance(value, list):
                        value = value[0]  # Take only the first value if not a list field
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
                    if PYDANTIC_1:
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias))
                        )
                    else:  
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

By making the changes above, the corrected function should now handle repeated keys in form data correctly, resolving the issue and passing the failing tests.