The bug in the `request_body_to_args` function is that it does not handle non-typing sequences correctly, leading to errors in processing lists, sets, and tuples passed in as form data.

The issue lies in how the function handles sequences in the input body when processing the received data. To fix this bug, we need to adjust the logic to correctly handle list, set, and tuple types when processing form data.

Here is a corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        for field in required_params:
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
                    if field.shape == 1:
                        value = value if isinstance(value, list) else [value]
                        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                        if isinstance(errors_, ErrorWrapper):
                            errors.append(errors_)
                        elif isinstance(errors_, list):
                            errors.extend(errors_)
                        values[field.name] = v_
                    elif field.shape == 2 and isinstance(value, list):  # Handle set
                        v_, errors_ = field.validate(set(value), values, loc=("body", field.alias))
                        if isinstance(errors_, ErrorWrapper):
                            errors.append(errors_)
                        elif isinstance(errors_, list):
                            errors.extend(errors_)
                        values[field.name] = v_
                    elif field.shape == 3 and isinstance(value, list):  # Handle tuple
                        v_, errors_ = field.validate(tuple(value), values, loc=("body", field.alias))
                        if isinstance(errors_, ErrorWrapper):
                            errors.append(errors_)
                        elif isinstance(errors_, list):
                            errors.extend(errors_)
                        values[field.name] = v_
    
    return values, errors
```

This corrected version of the function handles different types of sequences (list, set, tuple) correctly when processing form data. It converts the received data into the appropriate sequence type before validation to ensure that the input is processed correctly.

This fix should now allow the failing tests for lists, sets, and tuples passed as form data to pass successfully.