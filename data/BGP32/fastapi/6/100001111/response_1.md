The bug in the `request_body_to_args` function is related to handling multiple values for the same key in the received body, specifically when dealing with FormData. The function is not correctly parsing and handling the values of the received body, leading to issues with list, set, or tuple parameter types.

### Error Location:
The primary error in the function lies in how it processes the received body when multiple values are present for the same key.

### Bug Cause:
1. The function does not account for multiple values for the same key in FormData.
2. When iterating over multiple required params, the function incorrectly handles the values for each field's alias, leading to incorrect assignments and errors.

### Bug Fix Strategy:
1. Check for cases where multiple values are present for the same key in FormData.
2. Adjust the logic to properly handle and validate such cases for list, set, or tuple parameter types.

### Corrected Version of the Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []

    if received_body is None:
        received_body = {}

    for field in required_params:
        value = received_body.getlist(field.alias) if isinstance(received_body, FormData) else received_body.get(field.alias)

        if value is None or (isinstance(value, list) and len(value) == 0):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
                awaitables = [sub_value.read() for sub_value in value]
                contents = await asyncio.gather(*awaitables)
                value = tuple(contents) if field.shape == 1 else contents
            else:
                value = value if field.shape == 1 else [value]

            v_, errors_ = field.validate(value, values, loc=("body", field.alias))

            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_

    return values, errors
```

The corrected function now properly handles multiple values for the same key in FormData, ensuring that list, set, and tuple parameter types are correctly parsed and validated. This addressing the issue raised in the GitHub feature request.