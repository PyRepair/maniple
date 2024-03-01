### Bug Explanation
The bug in the `request_body_to_args` function arises from the handling of sequence shaped fields (list, set, tuple) passed as form data. The current implementation treats all sequence shaped fields as single values, leading to errors in validation and incorrect results.

For each case:
1. In Case 1, the function incorrectly treats the received form data as a single value instead of a list. This results in a validation error when validating against a list field.
2. In Case 2, the function incorrectly handles a set field as a single value, leading to validation errors and an incorrect return value.
3. In Case 3, the function wrongly interprets a tuple field as a single value, causing validation errors and an incorrect output.

### Proposed Fix
To fix the bug, the function needs to correctly handle sequence shaped fields in the form data. It should check if the field being processed is a sequence shape and then handle the received data accordingly.

Here is the corrected version of the function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        for field in required_params:
            field_info = get_field_info(field)
            embed = getattr(field_info, "embed", None)
            
            if lenient_issubclass(field.type_, Sequence):
                values[field.name] = received_body.getlist(field.alias) if received_body is not None else None
            else:
                value = received_body.get(field.alias) if received_body is not None else None
                
                if value is None or (isinstance(field_info, params.Form) and value == ""):
                    if field.required:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:
                        values[field.name] = deepcopy(field.default)
                else:
                    if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                        value = await value.read()
                    elif isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
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

By correctly differentiating between sequence-shaped fields and non-sequence fields, the corrected function should handle list, set, and tuple fields as expected, resolving the validation errors and ensuring the appropriate return values.