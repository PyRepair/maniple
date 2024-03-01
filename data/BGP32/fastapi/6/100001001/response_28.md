### Bug Explanation
The bug in the `request_body_to_args` function occurs when processing sequence types (such as lists, sets, or tuples) in the `received_body` parameter. The issue arises from how the function handles sequence types in the `received_body`, leading to incorrect validation and error generation.

### Bug Fix Strategy
1. Update the logic to correctly handle sequence types in the `received_body`.
2. Ensure that the function processes each sequence item individually when necessary.
3. Validate the values for sequence types according to their specific requirements.

### Corrected Version of the Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    sequence_shapes = {1}
    sequence_types = (tuple, list, set)
    sequence_shape_to_type = {1: tuple, 2: list}
    
    if required_params:
        field = required_params[0]
        field_info = get_field_info(field)
        embed = getattr(field_info, "embed", None)
        
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            
            if value is None or (isinstance(field_info, params.Form) and value == ""):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            
            if field.shape in sequence_shapes and isinstance(value, sequence_types):
                processed_values = []
                for sub_value in value:
                    if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(sub_value, UploadFile):
                        sub_value = await sub_value.read()
                    processed_values.append(sub_value)
                value = sequence_shape_to_type[field.shape](processed_values)
            
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    
    return values, errors
``` 

This corrected version of the function should handle sequence types correctly in the `received_body` parameter and validate them accordingly. It will avoid the erroneous behavior observed in the failing test cases.