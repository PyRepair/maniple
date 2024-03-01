### Bug Explanation
The bug in the `request_body_to_args` function arises from the incorrect handling of cases where the shape of the field is specified as a sequence (list, set, tuple) in the required parameters. The current implementation does not appropriately extract and validate the values from the received body for sequence-shaped fields, leading to errors and incorrect results.

### Bug Fix Strategy
To fix the bug:
1. Iterate over each field in the required parameters list.
2. Check if the field shape is a sequence type (list, set, tuple).
3. Extract the corresponding values from the received body based on the field alias.
4. Validate the extracted value and handle the cases where it is missing or needs further processing for sequence-shaped fields.
5. Update the `values` dictionary and `errors` list accordingly.

### Corrected Version of the Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        field_info = get_field_info(field)
        embed = getattr(field_info, "embed", None)
        
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
                values[field.name] = deepcopy(field.default)
        else:
            if field.shape in sequence_shapes and isinstance(value, sequence_types):
                if field_info.shape in [list, set]:
                    value = field.type_(value)
                else:  # tuple
                    value = tuple(field.type_(v) for v in value)
            else:
                if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
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

By following the provided bug fix strategy and updating the function as above, the `request_body_to_args` function should now correctly handle required parameters with sequence-shaped fields and extract values from the received body accordingly, ensuring proper validation and error handling.