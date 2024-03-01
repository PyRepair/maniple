The bug in the function `request_body_to_args` is due to incorrect handling of sequence types (list, set, tuple) when parsing the received body data. The function fails to properly extract values from the FormData object and process them according to the expected type.

### Bug Cause:
1. The function fails to properly handle sequence shapes when extracting values from the received body.
2. It incorrectly sets the value based on the received data, leading to errors in validation and building the final values dictionary.

### Bug Fix Strategy:
1. Ensure that the function correctly handles different sequence shapes (list, set, tuple) when processing the received body.
2. Extract the values from the FormData object based on the field alias and shape to correctly build the final values dictionary.
3. Update the logic to handle different types of values and validate them accordingly.

### Corrected Function:
Below is the corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value = None
        if received_body is not None:
            if field.alias in received_body.keys():
                value = received_body[field.alias]
        
        if value is None:
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
            continue
        
        if isinstance(field.type_, list):
            if not isinstance(value, list):
                value = [value]
        elif isinstance(field.type_, set):
            if not isinstance(value, set):
                value = {value}
        elif isinstance(field.type_, tuple):
            if not isinstance(value, tuple):
                value = (value,)
        
        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
        
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_
    
    return values, errors
```

This corrected version should now properly handle different sequence shapes (list, set, tuple) and extract the values from the FormData object to build the final values dictionary accordingly. It addresses the bug by correctly processing the received body data based on the expected field types.