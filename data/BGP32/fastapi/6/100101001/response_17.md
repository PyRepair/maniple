### Bug Explanation:
The buggy function `request_body_to_args` is failing to properly handle non-typing sequences like lists, sets, and tuples when passed as form data. It is incorrectly treating them as individual items instead of sequences, leading to errors in validation.

1. In each case, the function attempts to extract the value of the field from the received body, but it is doing so incorrectly for non-typing sequences. It should handle them as a whole sequence instead of individual elements.

2. The branch that mistakenly processes non-typing sequences uses a check on `field.shape` to determine if it is in `sequence_shapes`. This logic is not properly accounting for non-typing sequences, leading to erroneous handling.

### Strategy for Fixing the Bug:
To fix the bug, the function needs to correctly handle non-typing sequences such as lists, sets, and tuples as a whole entity rather than individual elements. This can be achieved by modifying the logic related to non-typing sequences in the function.

### Corrected Version of the Function:
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
                            ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig)
                        )
                else:
                    values[field.name] = deepcopy(field.default)
                    
            else:
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

By updating how the function handles non-typing sequences in the `request_body_to_args` function, the corrected version should now properly process non-typing sequences when passed as form data.