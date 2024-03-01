The bug in the `request_body_to_args` function seems to be related to how it handles sequence-shaped fields like lists, sets, and tuples when processing form data. The function is incorrectly extracting values from the `received_body` based on the shape of the field and generating errors or populating the `values` dictionary accordingly.

### Bug Cause Analysis:
1. The function is not correctly handling sequence-shaped fields in the case where the `received_body` is a `FormData`.
2. The function is not forming the correct values and errors lists when dealing with sequence-shaped fields.

### Bug Fix Strategy:
1. Check the shape of the field and handle it appropriately when the `received_body` is a `FormData`.
2. Validate and assign values correctly to the `values` dictionary and errors list based on the field's characteristics.

### Revised `request_body_to_args` Function:
```python
sequence_shapes = {1}  # Define the shapes for sequence fields like list, tuple, set

async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    for field in required_params:
        value: Any = None
        
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias, [])
                
        if (
            value is None
            or (isinstance(field_info, params.Form) and value == [])
            or (
                isinstance(field_info, params.Form)
                and field.shape in sequence_shapes
                and len(value) == 0
            )
        ):
            if field.required:
                errors.append(
                    ErrorWrapper(MissingError(), loc=("body", field.alias))
                )
            else:
                values[field.alias] = field.default
        else:
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.alias] = v_
    
    return values, errors
```

This revised function should now properly handle sequence-shaped fields in form data and correctly validate and assign values, leading to passing the failing tests with the expected input/output values.