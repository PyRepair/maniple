### Bug Explanation
The bug in the `request_body_to_args` function is related to how it handles different shapes of fields and their values when processing the received body data. In the cases of lists, sets, and tuples, the function fails to correctly extract and process the values from the FormData object, leading to an incorrect status code (422 instead of the expected 200) in the tests. This is primarily due to how the function processes the values for different types of data structures and sequences.

### Bug Fix Strategy
1. Ensure that the function correctly extracts values from FormData for different field shapes (lists, sets, tuples).
2. Handle the specific logic for each field shape to properly process and validate the received data.
3. Keep track of any errors encountered during validation to return appropriate error messages.
4. Refactor the function to improve readability and maintainability.

### Corrected Version of the Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    for field in required_params:
        value: Any = None
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                # Extract the correct value based on the field shape
                if field.shape == 1:
                    value = received_body.getlist(field.alias)
                elif field.shape == 2:
                    value = {item.decode("utf-8") for item in received_body.getlist(field.alias)}
                elif field.shape == 3:
                    value = tuple(item.decode("utf-8") for item in received_body.getlist(field.alias))
                else:
                    value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
        
        if value is None or value == "" or len(value) == 0:
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
            continue
        
        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_
    
    return values, errors
```

This corrected version of the function ensures that values are extracted correctly based on the field shape, processed appropriately, and any encountered errors are handled accordingly.