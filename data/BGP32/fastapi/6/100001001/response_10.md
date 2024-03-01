The bug in the `request_body_to_args` function is caused by incorrectly handling sequence shapes in the provided `required_params` and `received_body` data.

### Bug Explanation
1. When the function receives a list of required parameters and a dictionary of received data (or FormData), it iterates through the required parameters.
2. If the shape of the field in the parameter is a sequence and the received data is of type FormData, it tries to extract the value for that field using `getlist(field.alias)`.
3. The bug occurs when the code incorrectly extracts the values from the FormData object for sequence-shaped fields, leading to validation errors and incorrect data population.

### Bug Fix Strategy
To fix the bug, we need to correctly handle sequence-shaped fields when processing the received body data, ensuring the values are extracted and transformed appropriately based on the shape of the field.

### Corrected Function
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
        value = None
        
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.shape == 1:
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.getlist(field.alias)
                    
            else:
                value = received_body.get(field.alias)
                
        if value is None or (isinstance(field_info, params.Form) and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
            else:
                values[field.name] = deepcopy(field.default)
        else:
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

In the corrected function, we handle the extraction of values for sequence-shaped fields correctly using `getlist` for fields of shape 1 and differently for other shape types. We also address the validation process for these values according to their types and shapes.