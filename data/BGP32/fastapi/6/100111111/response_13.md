Based on the analysis provided, the bug in the function `request_body_to_args` stems from the incorrect handling of repeated keys in Form Data. The function fails to properly populate the values when the same key appears multiple times. To fix this issue, we need to modify the logic to handle repeated keys correctly.

Here is the corrected version of the `request_body_to_args` function that should resolve the failing tests and adhere to the expected input/output values:

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
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.alias in received_body.keys():
                    value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
        
        if value is None or (isinstance(field.info, params.Form) and value == ""):
            if field.required:
                errors.append(
                    ErrorWrapper(MissingError(), loc=("body", field.alias))
                )
            else:
                values[field.name] = deepcopy(field.default)
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

With these updated modifications, the function should now correctly handle repeated keys in Form Data and pass the failed tests provided. Please test the revised function and run the failing tests to ensure that it now produces the expected results.