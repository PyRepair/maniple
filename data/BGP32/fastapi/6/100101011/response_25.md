## Bug Analysis:
1. The buggy function `request_body_to_args` is responsible for converting received body data into arguments based on required model fields.
2. The bug is related to how the function handles sequence-shaped fields (list, set, tuple) when receiving form data.
3. The function incorrectly processes the data for sequence-shaped fields, leading to validation errors and incorrect values.
4. The bug affects situations where multiple values are provided for a single key, not being processed as expected.
5. The failing tests reflect the issue when trying to process list, set, and tuple data as form data.

## Bug Fix Strategy:
1. Modify the processing logic for sequence-shaped fields in the `request_body_to_args` function.
2. Update the way the function handles form data for sequence-shaped fields to correctly process multiple values for a single key.
3. Ensure that validation errors are generated correctly and that the values are extracted accurately from the received body.

## Bug-fixed version of the function:

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
            if embed:
                received_body = {field.alias: received_body}
            value: Any = None
            
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    if field.alias in received_body:
                        if field.shape == 1:
                            value = [received_body.get(field.alias)]
                        else:
                            value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
                    
            if value is None or (isinstance(field_info, params.Form) and value == "") or (
                isinstance(field_info, params.Form)
                and field.shape in sequence_shapes
                and len(value) == 0
            ):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
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

By modifying the handling of sequence-shaped fields in the function, the new version should correctly process repeated key-value pairs in form data and provide the expected output for the failing tests related to list, set, and tuple data sent as form data.