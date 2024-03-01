### Bug Fix Analysis:
1. The bug arises from incorrect handling of non-typing sequences (like list, set, tuple) passed as form data.
2. The function is not correctly converting the received form data into the expected types for non-typing sequence fields.
3. The bug is causing validation errors leading to a status code of 422 (validation error) instead of 200 (success).

### Bug Fix Strategy:
1. Update the function to correctly handle non-typing sequences (list, set, tuple) in form data.
2. Ensure that the values extracted from the form data are converted to the correct types expected by the fields.

### Corrected Function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        field = required_params[0]
        field_info = get_field_info(field)
        embed = getattr(field_info, "embed", None)
        
        if len(required_params) == 1 and not embed:
            received_body = {field.alias: received_body}
        
        for field in required_params:
            value: Any = None
            
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    if isinstance(field.type_, list):
                        value = received_body.getlist(field.alias)
                    elif isinstance(field.type_, set):
                        value = set(received_body.getlist(field.alias))
                    elif isinstance(field.type_, tuple):
                        value = tuple(received_body.getlist(field.alias))
                else:
                    value = received_body.get(field.alias)
            
            if (
                value is None
                or (isinstance(field_info, ModelField) and value == "")
                or (
                    isinstance(field_info, ModelField)
                    and field.shape in sequence_shapes
                    and len(value) == 0
                )
            ):
                if field.required:
                    if PYDANTIC_1:
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias))
                        )
                    else:
                        errors.append(
                            ErrorWrapper(
                                MissingError(),
                                loc=("body", field.alias),
                                config=BaseConfig,
                            )
                        )
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            
            if (
                isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif (
                field.shape in sequence_shapes
                and isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, sequence_types)
            ):
                awaitables = [sub_value.read() for sub_value in value]
                contents = await asyncio.gather(*awaitables)
                value = sequence_shape_to_type[field.shape](contents)
            
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    
    return values, errors
```

By updating the handling of non-typing sequences in form data within the `request_body_to_args` function, the corrected version should pass the failing tests and provide the expected output values for different scenarios.