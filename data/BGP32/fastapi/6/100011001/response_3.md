### Bug Analysis
1. The function `request_body_to_args` is designed to extract values from the received body (either a `Dict` or `FormData`) based on the required parameters passed to it.
2. The bug occurs when the function handles non-typing sequences (like lists, sets, and tuples) as form data.
3. The bug triggers a validation error, resulting in a status code of 422 instead of the expected 200.
4. The issue arises because the function does not handle non-typing sequences appropriately when validating the received data against the required parameters.
5. The error messages indicate that the error is related to sequence shapes and the validation process not correctly identifying the provided data.

### Bug Fix Strategy
1. Modify the function to handle non-typing sequences correctly when processing form data.
2. Update the validation process to account for different data structures, ensuring the correct values are extracted and validated.

### Corrected Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    sequence_types = (list, tuple, set)
    sequence_shapes = {1}

    if required_params:
        field = required_params[0]
        field_info = get_field_info(field)
        embed = getattr(field_info, "embed", None)
        if len(required_params) == 1 and not embed:
            received_body = {field.alias: received_body}
            
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    value = list(received_body.getlist(field.alias))
                else:
                    value = received_body.get(field.alias)
                
            if value is None or (isinstance(field_info, params.Form) and (not value or value == [""])):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
                continue
                
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                value = await value.read()
                
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    
    return values, errors
```

By updating the function with the corrected version, it should be able to handle non-typing sequences as form data correctly and pass the failing tests with the expected status code of 200.