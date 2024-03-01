### Bug Explanation:
The bug in the `request_body_to_args` function originates from the way it handles non-typing sequences (like lists, sets, tuples) when receiving input data as `FormData`. The function incorrectly tries to process these sequences as simple values instead of recognizing them as sequences. This results in errors being raised due to the mismatch in types when validating the received data against the expected field types.

### Bug Fix Strategy:
To fix the bug, we need to properly handle non-typing sequences in the `FormData` input. We should identify when a field is a sequence type and adjust our processing logic accordingly to correctly handle multiple values for the same key.

### Corrected Version of the Function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        # Check if received_body is a dict, in case it's a FormData
        if isinstance(received_body, FormData):
            received_body = received_body.multi_items()
        for field in required_params:
            value: Any = None
            if received_body is not None:
                value = received_body.get(field.alias)
            if value is None:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                    value = await value.read()
                elif field.shape in sequence_shapes and isinstance(value, sequence_types):
                    if field.shape == 1:
                        value = list(value)
                    elif field.shape == 2:
                        value = set(value)
                    elif field.shape == 3:
                        value = tuple(value)

                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
    return values, errors
```

After applying these corrections, the function should now correctly handle non-typing sequences when processing input data from `FormData`, ensuring that the tests pass successfully.