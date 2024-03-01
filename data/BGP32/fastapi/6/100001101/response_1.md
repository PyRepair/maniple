### Bug Explanation
The bug in the provided function is due to the incorrect handling of different shape types when processing the received body data. The function assumes that each field has a single value, which leads to errors when dealing with fields that can have multiple values like lists, sets, or tuples.

### Bug Fix Strategy
To fix the bug, we need to properly handle fields with different shapes and extract the values accordingly. This involves checking the shape of the field and handling sequences properly to capture all values. Additionally, we need to correctly populate the `values` dictionary with the extracted values.

### Corrected Function
Here is the corrected version of the `request_body_to_args` function:

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
                    values[field.name] = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
                    if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                        value = await value.read()
                    elif field.shape in sequence_shapes and isinstance(value, sequence_types):
                        values[field.name] = value
                
                if value is None or (isinstance(field_info, params.Form) and value == "") or \
                   (isinstance(field_info, params.Form) and field.shape in sequence_shapes and len(value) == 0):
                    if field.required:
                        if PYDANTIC_1:
                            errors.append(
                                ErrorWrapper(MissingError(), loc=("body", field.alias))
                            )
                        else:  # pragma: nocover
                            errors.append(
                                ErrorWrapper(  # type: ignore
                                    MissingError(),
                                    loc=("body", field.alias),
                                    config=BaseConfig,
                                )
                            )
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

This corrected version accounts for different shapes of fields correctly, handles sequences appropriately, and populates the `values` dictionary with the extracted values as expected.