### Bug Explanation:
The buggy function `request_body_to_args` has a bug related to the handling of fields with a sequence shape (like lists, sets, tuples) and the conversion of received data into the appropriate format. The function incorrectly handles the conversion of received data into a list, set, or tuple based on the type of the field.

The bug arises when processing `FormData` as the received data while dealing with sequence shape fields. The function fails to correctly parse the received data into the expected list, set, or tuple format, leading to errors in validation and wrong output values.

### Bug Fix Strategy:
To fix the bug, the function should properly handle the conversion of received data into the correct sequence shape based on the field definition. It should iterate over each value in the received data and process it according to the field's shape.

### Corrected Version:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    sequence_shapes = {1}
    for field in required_params:
        value = None
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.alias in received_body:
                    value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)

        if value is None or (isinstance(field.field_info, params.Form) and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
            continue

        if field.shape in {1} and lenient_issubclass(field.outer_type_, tuple):
            value = tuple(value)
        elif field.shape in {1} and lenient_issubclass(field.outer_type_, set):
            value = set(value)

        v_, errors_ = field.validate(value, values, loc=("body", field.alias))

        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_

    return values, errors
```

This corrected version properly handles the conversion of received data into the appropriate sequence shape based on the field definition, ensuring accurate validation and output values. It addresses the identified bug by appropriately processing the received data for fields with different sequence shapes.