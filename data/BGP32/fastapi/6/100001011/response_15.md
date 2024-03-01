### Problem Identification
- The function `request_body_to_args` is not handling the case where there are repeated keys in the `received_body`, causing issues with validation.
- The function does not aggregate the values of repeated keys into a list for validation.

### Bug Cause
- When there are repeated keys in the `received_body`, the function only considers the last value and discards the rest, leading to incomplete validation.
- The if condition checking for `len(required_params) == 1 and not embed` is not handling the scenario where there are multiple values for the same key.

### Fix Strategy
- Modify the function to aggregate the values of repeated keys into a list before validation.
- Check for repeated keys and consolidate their values to ensure proper validation.

### Corrected Version
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        for field in required_params:
            if isinstance(received_body, FormData):
                values[field.name] = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
                if value is not None:
                    values[field.name] = [value]
    
            for value in values[field.name]:
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
    
    return values, errors
```

This corrected version of the function aggregates the values of repeated keys in the `received_body` into a list, ensuring that all values are considered for validation.