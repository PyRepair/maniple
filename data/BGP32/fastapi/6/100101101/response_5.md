The bug in the provided function `request_body_to_args` lies in how it handles the input data when the field type is a collection (list, set, tuple) and the received body is of type FormData. The function incorrectly processes these cases, leading to errors in the test cases provided.

To fix the bug, we need to correctly extract the values for collection types from FormData and ensure that the values are stored in the correct format in the `values` dictionary.

Here is the corrected version of the function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if received_body is None:
        return values, errors
    
    for field in required_params:
        value: Any = received_body.get(field.alias)
        
        if value is None:
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
            continue
        
        if isinstance(field.type_, list):
            values[field.name] = value
        elif isinstance(field.type_, set):
            values[field.name] = set(value)
        elif isinstance(field.type_, tuple):
            values[field.name] = tuple(value)
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

This fixed version of the function correctly handles the conversion of values for collection types (list, set, tuple) when the received body is of type FormData. The function now correctly extracts the values and stores them in the expected format in the `values` dictionary.

This corrected version should now pass the failing test cases provided.