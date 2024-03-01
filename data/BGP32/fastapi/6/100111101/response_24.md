### Bug Explanation

The bug in the `request_body_to_args` function arises from how it handles complex shape types (like lists, sets, and tuples) when received as form data. At the beginning of the function, it tries to extract the values from the received form data based on the field aliases but doesn't handle the extraction correctly for sequences like lists, sets, and tuples.

For instance, in Case 1, where the required parameter is a list and the received form data contains multiple values for the same alias, the function incorrectly converts the values into individual strings instead of collecting them into a list. This leads to validation errors and ultimately returns incorrect output.

### Bug Fix Strategy

To fix the bug, the function should be modified to correctly handle the extraction and processing of complex shape types (lists, sets, tuples) from the form data. Specifically, when dealing with sequence shapes, the function should accumulate values with the same alias into the corresponding sequence structure instead of treating them individually.

### Corrected Function

Here is the corrected version of the `request_body_to_args` function:

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
                    if field.shape == 1:
                        value = received_body.getlist(field.alias)
                    else:
                        value = [received_body.get(field.alias)]
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
                    values[field.alias] = deepcopy(field.default)
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
                values[field.alias] = v_
    return values, errors
```

By appropriately handling the parsing and grouping of values in the form data based on the field aliases and shapes, the corrected function should now pass the failing tests and provide the expected output.