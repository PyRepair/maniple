### Analysis
1. The `request_body_to_args` function is designed to convert received body parameters to arguments based on the required parameters list. It loops through the required parameters, retrieves values from the received body, validates them, and collects any errors encountered.
2. The bug seems to be related to handling sequence-shaped fields like lists, sets, and tuples incorrectly, resulting in validation errors and a status code of 422.
3. The failing tests are for different types of non-typing sequences: list, set, and tuple. The current implementation fails to correctly process these sequence-shaped fields and results in validation errors.
4. To fix the bug, we need to properly handle the conversion of sequence-shaped fields from the request body to the expected Python types, ensuring that the validation process succeeds for these fields.

### Bug Fix Strategy
1. Identify and fix the incorrect handling of sequence-shaped fields (lists, sets, tuples) in the `request_body_to_args` function.
2. Ensure that the values extracted from the request body for such sequence-shaped fields are correctly processed and validated before returning them.

### Bug Fix
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        for field in required_params:
            field_info = get_field_info(field)
            value: Any = None
            
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            
            if value is None or (isinstance(field_info, params.Form) and value == ""):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                # Handle sequence-shaped fields correctly
                if field.shape in sequence_shapes:
                    if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                        if isinstance(value, UploadFile):
                            value = await value.read()
                    elif isinstance(value, list):
                        # Convert to correct Python type for sequence-shaped field
                        if field.shape == 1:
                            value = tuple(value) if field.type_ == tuple else set(value)
                        else:
                            errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
    
    return values, errors
```

With this fix, the `request_body_to_args` function should correctly handle sequence-shaped fields from the request body and successfully validate them for the given test cases.