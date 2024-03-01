### Bug Explanation
The bug in the `request_body_to_args` function is caused by the incorrect handling of non-typing sequences such as lists, sets, and tuples when they are passed as form data. The function fails to properly extract and validate values for these non-typing sequence types, resulting in errors being added to the `errors` list instead of correctly populating the `values` dictionary.

### Bug Fix Strategy
To fix the bug, we need to modify the logic within the function to correctly handle non-typing sequences like lists, sets, and tuples when they are passed as form data. This involves properly retrieving the values from the form data based on the field alias, validating the values, and populating the `values` dictionary accordingly without raising errors.

### Corrected Version of the Function
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
        
        for field in required_params:
            value: Any = None
            if received_body is not None:
                value = received_body.get(field.alias)
            
            if value is None and field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                    if isinstance(value, UploadFile):
                        value = await value.read()
                elif field.shape in sequence_shapes and isinstance(value, sequence_types):
                    if field.type_ in [list, set, tuple]:
                        value = value.values()
                        
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
    
    return values, errors
```

With this correction, the function now properly handles non-typing sequences like lists, sets, and tuples when they are passed as form data, ensuring that the values are correctly extracted, validated, and added to the `values` dictionary.