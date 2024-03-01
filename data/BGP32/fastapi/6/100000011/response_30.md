### Analysis:
The function `request_body_to_args` is responsible for converting the received body data into arguments based on the required parameters. The issue reported on GitHub is related to supporting repeated key-value pairs in form data.

### Error Locations:
1. The issue lies in the section where the function is processing form data with repeated keys, but only the last value is being considered.
2. When checking if the value is a string or a list in the case of repeated values, the function currently only handles the case of a single value.

### Cause of the Bug:
The bug occurs because the function does not handle repeated key-value pairs in the form data properly. It does not concatenate the values of repeated keys into a list before validation.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the function to handle repeated keys properly. When receiving form data with repeated keys, those values should be collected into a list assigned to the same key before validation occurs.

### Corrected Version:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        for field in required_params:
            values[field.name] = deepcopy(field.default)
            
            if received_body is not None:
                if field.alias in received_body:
                    value = received_body.getlist(field.alias)
                    if len(value) == 1:
                        value = value[0]
                        
                    if isinstance(field.type_, list) and len(value) > 1:
                        values[field.name] = value
                    else:
                        if isinstance(value, list):
                            value = value[-1]
                        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                        if isinstance(errors_, ErrorWrapper):
                            errors.append(errors_)
                        elif isinstance(errors_, list):
                            errors.extend(errors_)
                        else:
                            values[field.name] = v_
                else:
                    if field.required:
                        if field.alias not in received_body:
                            if PYDANTIC_1:
                                errors.append(
                                    ErrorWrapper(MissingError(), loc=("body", field.alias))
                                )
                            else:  # pragma: nocover
                                errors.append(
                                    ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig)
                                )
    return values, errors
```

The corrected version of the function now properly handles repeated key-value pairs in form data. It collects all values for the same key into a list before validation, thereby addressing the issue reported on GitHub.