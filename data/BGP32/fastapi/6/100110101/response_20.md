### Analysis:
1. The buggy function `request_body_to_args` is designed to extract values from the received body based on required parameters and return a tuple containing the extracted values and any errors encountered.
2. The function loops through required parameters to process each one individually.
3. The bug appears to be related to handling sequence types (list, set, tuple).
4. The failing test cases involve passing list, set, and tuple values in the body, causing the function to return a 422 error instead of 200.

### Bug:
The bug is likely in the logic for extracting values from the received body, especially when dealing with sequence shapes like lists, sets, and tuples. The function doesn't correctly handle these cases, leading to validation errors and returning the wrong status code.

### Bug Fix Strategy:
1. Ensure proper handling of sequence-shaped fields (list, set, tuple) when extracting values.
2. Verify that the values extracted match the expected data structure (list, set, tuple) based on the field type.

### Corrected Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    sequence_shapes = {1}
    for field in required_params:
        value: Any = None
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
        if value is None:
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = field.default
            continue
        if field.shape in sequence_shapes:
            value = value if isinstance(value, list) else [value]
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
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

This corrected version of the function contains the necessary code adjustments to handle sequence-shaped fields correctly when extracting values. It ensures that the extracted values match the expected data structure based on the field type.