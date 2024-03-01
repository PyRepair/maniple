### Bug Analysis:
- The bug appears to be related to how the function handles different types of input data (FormData) for parameters that are lists, sets, or tuples.
- The function checks if the input data is a FormData object, but it may not correctly extract the values for certain types like sets and tuples.
- It seems that the function might be failing to process and validate the input FormData correctly based on the field shape and the type of data expected.

### Bug Fix Strategy:
- Ensure that the function correctly handles different data shapes and types when extracting values from the input FormData object.
- Verify that the values extracted from FormData are correctly validated and processed based on the type and shape of the field.

### Correction:
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
            embed = getattr(field_info, "embed", None)
            if (
                len(required_params) == 1
                and not embed
                and field.alias in (received_body or {})
            ):
                received_body = {field.alias: received_body.get(field.alias)}
            
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
                                MissingError(), loc=("body", field.alias), config=BaseConfig
                            )
                        )
                else:
                    values[field.name] = deepcopy(field.default)
                continue

            if isinstance(value, list) and field.shape != 0:
                if field.shape in sequence_shapes:
                    v_ = []
                    for sub_value in value:
                        v_, errors_ = field.validate(sub_value, values, loc=("body", field.alias))
                        if isinstance(errors_, ErrorWrapper):
                            errors.append(errors_)
                        elif isinstance(errors_, list):
                            errors.extend(errors_)
                        else:
                            v_.append(v_)
                    values[field.name] = v_
                else:
                    v_ = []
                    for sub_value in value:
                        v_, errors_ = field.validate(sub_value, values, loc=("body", field.alias))
                        if isinstance(errors_, ErrorWrapper):
                            errors.append(errors_)
                        elif isinstance(errors_, list):
                            errors.extend(errors_)
                        else:
                            v_.append(v_)
                    values[field.name] = v_
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

### Correction Rationale:
- The corrected function now properly handles different data shapes and types by checking if the field shape is a sequence shape before processing the values.
- It correctly validates and processes the extracted values based on the field shape and type, improving the overall handling of input data for different types of parameters.