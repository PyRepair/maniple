### Bug Explanation:
The bug occurs in the `request_body_to_args` function when handling non-typing sequences like lists, sets, and tuples. It fails to correctly handle these data structures and raises validation errors, leading to incorrect HTTP status codes (422 instead of the expected 200) in the failing test cases.

The root cause of the bug lies in how the function processes the received body data for non-typing sequences. The function expects the body data to be structured in a specific way based on the field type, but it doesn't handle non-typing sequences properly, resulting in validation errors and incorrect return values.

### Bug Fix Strategy:
1. Update the function to correctly handle non-typing sequences like lists, sets, and tuples by extracting the values based on their respective types.
2. Ensure that the function processes non-typing sequences appropriately for validation and data extraction.
3. Fix any conditional logic related to sequence types in the function to handle different cases correctly.

### Corrected Version of the Buggy Function:
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
            field_info = get_field_info(field)
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    value = received_body.getlist(field.alias)
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

### Key Changes Made:
1. Iterate over each field in the `required_params` list and extract the value based on the received body data.
2. Correctly handle the processing of non-typing sequences by adjusting conditional logic and extracting values accordingly.
3. Ensure that values are validated and added to the final result dictionary appropriately.

By applying these changes, the corrected function should now handle non-typing sequences correctly and pass the failing tests without raising validation errors.