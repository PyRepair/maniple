### Bug Explanation
The bug in the provided function `request_body_to_args` arises from the incorrect handling of sequence types in the input `received_body`. When the received body is a `FormData` and the expected type of the field is a sequence (e.g., list, set, tuple), the function doesn't handle this case properly. This leads to errors in validation and populating the `values` dictionary.

### Bug Fix
To fix the bug, the function should correctly handle cases where the expected type is a sequence (list, set, tuple) when the received body is a `FormData`. Here is the corrected version of the function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        field = required_params[0]
        field_info = get_field_info(field)
        embed = getattr(field_info, "embed", None)
        if len(required_params) == 1 and not embed:
            received_body = {field.alias: received_body}
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    if field.shape in sequence_shapes:
                        value = received_body.getlist(field.alias)
                    else:
                        value = received_body.get(field.alias)
                else:
                    value = received_body.get(field.alias)
            if value is None and field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                    if field.shape in sequence_shapes and isinstance(value, sequence_types):
                        awaitables = [sub_value.read() for sub_value in value]
                        contents = await asyncio.gather(*awaitables)
                        value = sequence_shape_to_type[field.shape](contents)
                    else:
                        value = await value.read()
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
    return values, errors
```

By ensuring correct handling of sequence types (list, set, tuple) in the `received_body`, the corrected function should now be able to properly validate and extract data from the input.