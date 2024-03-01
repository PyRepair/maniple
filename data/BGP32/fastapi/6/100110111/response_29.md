### Analysis:
1. The `request_body_to_args` function is responsible for extracting values from the received body data based on the required parameters provided.
2. The bug seems to be related to how the function handles repeated keys in form data and extracts values.
3. The failing tests indicate that the function is not correctly handling list, set, and tuple types in the form data, leading to status code 422 (validation error) instead of 200 (success).
4. The bug is likely due to how values are processed when handling sequence shapes and form data.

### Bug Cause:
The bug appears to stem from how the function handles repeated keys in form data for sequence shapes like lists, sets, and tuples. The function doesn't properly process or validate these values, leading to validation errors instead of successful extraction.

### Fix Strategy:
To address the bug and support repeated key=value pairs in form data for various sequence shapes, we need to:
1. Handle repeated keys correctly to accumulate values into lists, sets, or tuples depending on the field type.
2. Ensure that the function correctly extracts and processes these values to ultimately pass the validation checks.

### Corrected Version:
Here is the corrected version of the `request_body_to_args` function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        for field in required_params:
            value = None
            
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
                
            if value is None or value == "":
                if field.required:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if field.shape in sequence_shapes and isinstance(value, list):
                    v_ = value
                elif field.shape in sequence_shapes and isinstance(value, (set, tuple)):
                    v_ = value
                else:
                    v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                    
                    if isinstance(errors_, ErrorWrapper):
                        errors.append(errors_)
                    elif isinstance(errors_, list):
                        errors.extend(errors_)
                    else:
                        values[field.name] = v_

    return values, errors
```

This corrected version should now properly handle repeated keys in form data for various sequence shapes and provide the expected output values, resolving the issue reported in GitHub.