The bug in the `request_body_to_args` function lies in the handling of sequence shapes (list, set, tuple) when processing the received body data. The function incorrectly creates a list of values even for non-list shapes, leading to incorrect validation and errors.

To fix the bug, we need to adjust the logic in the function to properly handle different sequence shapes. We should handle the received body data according to the shape of the field being processed and validate it accordingly.

Here is the corrected version of the function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    for field in required_params:
        value: Any = None
        field_info = get_field_info(field)
        if received_body is not None:
            if isinstance(received_body, FormData):
                value = received_body.getlist(field.alias) if field.shape in sequence_shapes else received_body.get(field.alias)
                
        if value is None or (isinstance(field_info, params.Form) and not value):
            if field.required:
                errors.append(
                    ErrorWrapper(MissingError(), loc=("body", field.alias))
                )
            else:
                values[field.name] = deepcopy(field.default)
        
        elif isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
            value = await value.read()
        
        elif field.shape in sequence_shapes and isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
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

With the corrected function, the received body data will be processed correctly based on the shape of the field being processed.

Ensure to test the corrected function with the provided cases to validate its correctness.