### Analysis:
1. The function `request_body_to_args` is responsible for converting the received body data into arguments for request processing.
2. The failing tests are related to sending different types of non-typing sequences such as list, set, and tuple.
3. The error message indicates that the status code returned by the API is 422 instead of the expected 200.
4. The current implementation doesn't handle repeated keys in form data correctly, leading to incorrect validation results.
5. The bug is caused by improper handling of repeated keys in form data, impacting the validation of non-typing sequences.
6. To fix the bug, the function needs to correctly handle repeated keys in the form data and convert them into corresponding list, set, or tuple values before validation.

### Fix Strategy:
1. Modify the function to properly handle repeated keys in form data.
2. Convert repeated keys into a single key with a list of corresponding values.
3. Update the logic to support validation of non-typing sequences like list, set, and tuple.

### Corrected Version:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if received_body is not None and isinstance(received_body, FormData):
        received_dict = dict(received_body)
        repeated_keys = {key: value for key, value in received_dict.items() if len(value) > 1}
        
        for key, value in repeated_keys.items():
            received_dict[key] = value if len(value) > 1 else value[0]  # convert repeated key values to a list
        
        for field in required_params:
            if field.alias in received_dict:
                value = received_dict[field.alias]
                
                if isinstance(value, list) and field.shape in sequence_shapes:
                    values[field.alias] = value
                else:
                    values[field.name] = value
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                
    return values, errors
```

In the corrected version, we handle repeated keys in the form data and convert them to lists before validation. This approach ensures proper handling of non-typing sequences.