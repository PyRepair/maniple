The bug in the `request_body_to_args` function is related to handling repeated keys in form data. The function fails to correctly parse and assign values when the same key appears multiple times in the form data. This issue is reported in the GitHub problem regarding supporting repeated key=value pairs in form data.

### Error Location:
The main issue in the current implementation lies in how the function processes form data with repeated keys. When a key appears more than once in the form data, the function overrides the previous value instead of collecting all values under the same key.

### Cause of the Bug:
1. The function overwrites values for the same key in form data instead of aggregating them into a list.
2. It doesn't handle cases where a key appears multiple times and treats each occurrence as a separate value.

### Strategy for Fixing the Bug:
To fix the bug, the function needs to be modified to correctly handle repeated keys in form data and aggregate values under the same key into a list, tuple, or set based on the field type.

### Corrected Version of the Function:
Below is the corrected version of the `request_body_to_args` function that addresses the bug:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []

    if required_params:
        for field in required_params:
            value = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    values.setdefault(field.name, [])
                    values[field.name].extend(received_body.getlist(field.alias))
                else:
                    if field.alias in received_body:
                        values[field.name] = received_body.get(field.alias)

            if field.required and (value is None or value == ''):
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))

                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_

    return values, errors
```

This corrected version properly aggregates values for repeated keys in form data under the same key in the output dictionary. It handles the cases where a key appears multiple times by collecting all corresponding values.