### Bug Explanation:
The bug in the `request_body_to_args` function is related to handling form data for non-typing sequences like lists, sets, and tuples. When processing these sequences in the `received_body` FormData, the function fails to correctly extract the values based on the field alias.

The key issue lies in how the function processes the received body for these non-typing sequences. Specifically, the function incorrectly assumes that the value in the FormData corresponds directly to the field alias, leading to errors in processing and validation.

### Bug Fix Strategy:
To fix the bug, we need to adjust the logic for extracting values from the FormData when the field represents a non-typing sequence like a list, set, or tuple. By properly handling these cases and extracting values based on the correct alias, we can ensure that the values are processed correctly to match the expected input/output behavior.

### Corrected Function:
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
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    if isinstance(field.alias, str):
                        value = received_body.getlist(field.alias)
                    else:
                        value = [received_body.getlist(alias) for alias in field.alias]
                else:
                    value = received_body.get(field.alias)

            if value is None or (isinstance(field_info, params.Form) and value == "") or (
                isinstance(field_info, params.Form)
                and field.shape in sequence_shapes
                and len(value) == 0
            ):
                if field.required:
                    if PYDANTIC_1:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:  # pragma: nocover
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig,)
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

This corrected version should address the bug related to non-typing sequences in the `received_body` FormData and ensure that the function processes the values correctly for lists, sets, and tuples. It should now pass the failing tests and produce the expected input/output values.