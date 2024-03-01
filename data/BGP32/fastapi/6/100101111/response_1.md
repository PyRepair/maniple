### Bug Explanation

The bug in the `request_body_to_args` function lies in how it handles sequence shapes like `list`, `set`, and `tuple` for form data. The function fails to correctly extract and validate the values of these sequence shapes from form data, leading to errors in the test cases provided.

The function incorrectly processes the form data by expecting it to directly correspond to the required model fields without properly handling sequences. This results in errors during validation and incorrect extraction of values from form data.

### Bug Fix Strategy

To fix the bug, the function needs to handle sequence shapes properly when extracting values from form data. The function should differentiate between single and repeated occurrences of keys in form data and transform them into the appropriate sequence shape before validation.

### Corrected Function

Here is the corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if received_body is not None:
        for field in required_params:
            value: Any = None
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.alias in received_body:
                    if field.shape == 1:
                        value = [received_body[field.alias]]
                    elif field.shape == 2:
                        value = {received_body[field.alias]}
                    else:
                        value = (received_body[field.alias],)
                else:
                    if field.required:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:
                        values[field.name] = deepcopy(field.default)
            else:
                value = received_body.get(field.alias)
                
            if value is not None and value != "":
                if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                    value = await value.read()
                    
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
            else:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
    
    return values, errors
```

By making these changes, the function now properly handles sequence shapes for form data and extracts values accordingly. This corrected version should pass the failing test cases and resolve the issue reported on GitHub.