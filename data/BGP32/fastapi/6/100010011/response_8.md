### Analysis:
1. The function `request_body_to_args` is responsible for converting the incoming request body into arguments.
2. The failing tests indicate that the response status code is 422 (unprocessable entity) instead of the expected 200 (success).
3. The issue in GitHub mentions the problem of repeated key-value pairs in form data not being handled correctly.
4. The bug seems to stem from the handling of sequence shapes (lists, sets, tuples) in the input data.

### Bug Cause:
1. The function does not handle the case of repeated values for a key properly.
2. When multiple values with the same key are present in the form data, only the last value is being considered due to the usage of methods like `received_body.get()` which only extract a single value for a key.
3. This behavior leads to validation errors as the function expects each key-value pair to be unique.

### Bug Fix Strategy:
To resolve this bug and support repeated key-value pairs for sequence shapes in form data:

1. Check if a field is part of a sequence shape and handle repeated values for the same field key properly.
2. Collect all values for a repeated key, and store them in a list to pass for validation.
3. Allow the function to accept multiple values for the same key.

### Corrected Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = {}
    
    if received_body is None:
        received_body = {}

    for field in required_params:
        values[field.name] = []
        value = received_body.get(field.alias)
        
        if value is not None:
            if field.shape in sequence_shapes and isinstance(value, FormData):
                value = value.getlist(field.alias)
            
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                value = await value.read()
            elif field.shape in sequence_shapes and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
                awaitables = [sub_value.read() for sub_value in value]
                value = await asyncio.gather(*awaitables)
                value = sequence_shape_to_type[field.shape](value)
            
            values[field.name] = value

    return values, errors
```
In the corrected version, we iterate over each required parameter, handle repeated values for the same key appropriately, and store the values in a list. This change allows the function to properly collect all values for repeated keys and pass them for validation.

By making these adjustments, the function should now process sequence shapes in form data correctly and pass the modified tests, resolving the GitHub issue.