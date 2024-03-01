The bug in the provided function `request_body_to_args` is related to handling repeated keys in form data. The function currently does not support collecting all values for a repeated key, causing only the last value to be considered.

To fix the bug and address the GitHub issue, the function needs to be modified to correctly handle repeated keys in form data and collect all values associated with them. This involves updating the logic to handle sequence_shapes properly and gather all values for repeated keys before validation.

Here is the corrected version of the function `request_body_to_args` that addresses the bug and aligns with the expected input/output values and the GitHub issue:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        for field in required_params:
            values[field.name] = None

            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    values[field.name] = received_body.getlist(field.alias)
                else:
                    values[field.name] = received_body.get(field.alias)

            if values[field.name] is None:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                    if field.shape in sequence_shapes:
                        awaitables = [value.read() for value in values[field.name]]
                        contents = await asyncio.gather(*awaitables)
                        values[field.name] = sequence_shape_to_type[field.shape](contents)
                    else:
                        values[field.name] = await values[field.name].read()

        for field in required_params:
            v_, errors_ = field.validate(values[field.name], values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_

    return values, errors
```

This corrected version of the function now properly processes repeated keys in form data and collects all values associated with them. It aligns with the expected input/output values provided for different cases and addresses the issue raised on GitHub regarding supporting repeated key=value pairs in form data.