### Bug Explanation:
The buggy function `request_body_to_args` fails to correctly handle the scenario where the input parameter `received_body` is a `FormData` object containing multiple values with the same key. In such cases, the function should extract all values associated with that key and process them appropriately. However, the current implementation only considers the first value associated with the key, leading to incorrect processing and output.

### Bug Location:
The issue lies within the loop where the function iterates over the `required_params` list. Specifically, when the condition `len(required_params) == 1 and not embed` is met, the function incorrectly sets the `received_body` dictionary to only contain the first value associated with the key, instead of all values.

### Proposed Fix:
To address the bug, we need to ensure that when handling `FormData` objects with multiple values for the same key, we correctly extract and process all of these values. This can be achieved by modifying the logic that deals with multiple values for the same key in the `FormData` object.

### Corrected Version of the Function:
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
                    if field.alias in received_body.keys():
                        if field.shape == 1:
                            value = received_body.getlist(field.alias)
                        elif field.shape == 2:
                            value = received_body.get(field.alias)
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

By making the changes outlined in the corrected version above, the `request_body_to_args` function should now be able to correctly process `FormData` objects with multiple values for the same key and provide the expected output for the provided failing tests.