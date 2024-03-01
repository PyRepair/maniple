### Bug Analysis:
- The bug originates from the fact that the function is not correctly handling the case when the received data is a non-typed sequence (like a list, set, or tuple) passed as form data.
- The function is not properly converting the received data into the correct Python native data structure before returning the values.

### Bug Fix Strategy:
- Modify the function to handle non-typed sequences properly by converting the data appropriately based on the type of the field.
- Update the logic to extract the data from FormData correctly and convert it to the expected Python data structure.
- Ensure that the error handling for missing required fields is done accurately.

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
            field_info = get_field_info(field)
            embed = getattr(field_info, "embed", None)
            if len(required_params) == 1 and not embed:
                received_body = {field.alias: received_body}
            value: Any = None
            if received_body is not None:
                value = received_body.getlist(field.alias) if field.shape in sequence_shapes else received_body.get(field.alias)
            
            if value is None or value == []:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            
            if field.shape in sequence_shapes:
                if lenient_issubclass(field.type_, bytes):
                    if isinstance(value, list):
                        v_ = value  # No need to convert the list
                    elif isinstance(value, sequence_types):
                        contents = [await sub_value.read() for sub_value in value]
                        v_ = sequence_shape_to_type[field.shape](contents)
                    else:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
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

The corrected function properly handles the case when non-typed sequence data is passed as form data and converts it to the expected Python data structure, ensuring that the function now returns the correct values according to the specified input parameters.