### Bug Explanation:
The bug in the `request_body_to_args` function occurs due to an incorrect handling of non-typing sequences (list, set, tuple) passed as form data. The function is designed to process received form data and convert it into arguments based on the required params. However, when a non-typing sequence is passed in the form data, the function fails to extract the correct values due to incorrect handling of fields.

The bug causes the function to fail validation checks and return a status code of 422 (Unprocessable Entity) instead of the expected 200 (OK) response status.

### Bug Fix Strategy:
To fix the bug, the function needs to correctly handle non-typing sequence shapes (list, set, tuple) when passed as form data. This includes ensuring that the values are appropriately extracted and processed to match the expected field specifications.

### Corrected Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        for field in required_params:
            value: Any = None
            
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
                    
            if value is None:
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
                
            if isinstance(field_info, params.File):
                if lenient_issubclass(field.type_, bytes):
                    if isinstance(value, UploadFile):
                        value = await value.read()
                    elif isinstance(value, sequence_types):
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

By correcting the function to appropriately handle non-typing sequences passed as form data, the issues encountered in the failing test cases should be resolved, and the function should return the expected values.