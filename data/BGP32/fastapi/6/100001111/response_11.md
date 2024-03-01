### Bug Explanation
The bug arises from the incorrect handling of repeated keys in form data, causing only the last key=value pair to be processed in the provided function `request_body_to_args`. This leads to incorrect validation results when multiple values for the same key are expected.

### Bug Location
The main issue lies in the way the function processes received form data when dealing with sequence shapes and repeated keys.

### Bug Cause
1. The function sets the `received_body` dictionary to have a single key-value pair when dealing with a single field without considering multiple inputs for the same key.
2. When trying to retrieve values for fields with repeated keys (in the form of lists, sets, or tuples), the function does not handle these sequence shapes appropriately, leading to validation issues.

### Fix Strategy
To address the bug and fulfill the requirements of the expected test cases and the GitHub issue, the function should be modified to properly handle repeated keys in the form data and correctly validate the values for fields with sequence shapes.

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
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.getlist(field.alias) if isinstance(received_body, FormData) else received_body.get(field.alias, [])
            if value is None or (isinstance(field_info, params.Form) and value == ""):
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
                and all(isinstance(v, UploadFile) for v in value)
            ):
                awaitables = [v.read() for v in value]
                contents = await asyncio.gather(*awaitables)
                if field.shape in sequence_shapes:
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

This corrected version now properly handles repeated keys in form data and validates values for fields with sequence shapes according to the expected behavior and the proposed solution in the GitHub issue.