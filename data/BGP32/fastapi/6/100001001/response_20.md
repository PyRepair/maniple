### Bug Explanation
The bug in the `request_body_to_args` function occurs when processing values received in the `received_body` against the required parameters `required_params`. The function tries to handle multiple items with the same field alias by grouping them into a dictionary, but some validations and error handling are not correctly performed for sequence-shaped fields like lists, sets, and tuples.

### Bug Fix Strategy
1. Ensure that the function correctly handles sequence-shaped fields and retrieves values properly from FormData.
2. Perform appropriate error handling based on the shape of the field and the presence of values.
3. Validate the received values against the defined field types and handle any errors accordingly.

### Corrected Version of the Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        for field in required_params:
            value: Any = None
            
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            
            if value is None:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))  
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
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

In the corrected version:
- Proper handling of sequence-shaped fields like lists, sets, and tuples is included.
- Correct error handling based on field shape and presence of values is implemented.
- Validation of received values against the defined field types is performed, and errors are handled appropriately.