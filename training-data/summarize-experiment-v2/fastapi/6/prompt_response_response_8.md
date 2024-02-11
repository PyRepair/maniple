The issue here is related to handling repeated keys in form data. The bug seems to be in the `request_body_to_args` function, specifically in the handling of repeated keys in form data. The function does not handle repeated keys as expected when using FastAPI's validation for lists, sets, and tuples.

The failing test cases are expecting a 200 status code, but receiving a 422 status code, indicating a validation error in the `request_body_to_args` function.

The GitHub issue title for this bug could be "Support repeated key=value in form data", and the detailed description could explain the problem and propose a solution. The proposed solution suggests that FastAPI should collect repeated keys in the form data and assign those values as a list to the same key before validation happens.

To fix this bug, the `request_body_to_args` function needs to be updated to correctly handle repeated keys in form data. Specifically, it needs to collect repeated keys and assign those values as a list to the same key before validation.

Here's the corrected code for the `request_body_to_args` function:

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
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            if (
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

In the corrected code, the function iterates through the required parameters and properly handles repeated keys in form data, assigning them as a list to the same key before validation.

With this correction, the `request_body_to_args` function should now correctly handle repeated keys in form data and pass the failing tests, thus addressing the GitHub issue and resolving the bug.