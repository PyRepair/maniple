### Bug Explanation
The issue in the provided function arises from incorrectly formatting a sequence of items in the `received_body` when the sequence is not embedded. For example, if the `received_body` contains multiple values for a parameter defined as a list, set, or tuple in the `required_params`, the current implementation does not handle these cases correctly, leading to errors and incorrect values in the output.

### Bug Fix Strategy
To address the bug, we need to modify how the function handles multiple values for the same field in the `received_body` based on the type of the field (list, set, tuple). We should ensure that each field in the `required_params` is processed correctly in alignment with its shape.

### Corrected Version of the Function
Here is the corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        field_info = get_field_info(field)
        value: Any = None
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(
                received_body, FormData
            ):
                if field.alias in received_body:
                    raw_values = received_body.getlist(field.alias)
                    if field.shape is list:
                        value = raw_values
                    elif field.shape is set:
                        value = set(raw_values)
                    elif field.shape is tuple:
                        value = tuple(raw_values)
                else:
                    value = None
            else:
                value = received_body.get(field.alias)
        
        if value is None:
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            # Add logic for File handling here if needed
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    
    return values, errors
```

This corrected version ensures that each field in the `required_params` list is correctly processed based on its shape, dealing with list, set, and tuple types appropriately when multiple values are present in the `received_body`.