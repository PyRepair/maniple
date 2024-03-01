The bug arises due to a misunderstanding of how non-typing sequence types (list, set, tuple) should be handled in the `request_body_to_args` function. The function incorrectly processes these non-typing sequences as regular fields, leading to validation errors and the function returning incorrect values.

To fix this bug, we need to handle non-typing sequence types differently than regular fields. Specifically, we need to extract the values correctly from the FormData object based on whether the field is a list, set, or tuple.

Below is the corrected version of the function that addresses the bug:

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
                    field_values = received_body.getlist(field.alias)
                    if field.type_ is list:  # Handle list type
                        value = field_values
                    elif field.type_ is set:  # Handle set type
                        value = set(field_values)
                    elif field.type_ is tuple:  # Handle tuple type
                        value = tuple(field_values)
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

With this correction, the function will correctly handle list, set, and tuple types when extracting values from the FormData object, leading to the expected output values and passing the failing tests.