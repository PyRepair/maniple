The bug in the provided function `request_body_to_args` lies in the logic for handling sequence shapes such as lists, sets, and tuples. The current implementation fails to extract the values correctly from the received body when dealing with sequences. Additionally, the assignment of the `embed` variable based on the first `required_params` element is not appropriate for all cases.

To fix this bug, we need to iterate over all required parameters and handle each field individually based on its shape and type. It's essential to properly extract the values from FormData for each parameter.

Here is the corrected version of the function `request_body_to_args`:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    for field in required_params:
        field_info = get_field_info(field)
        embed = getattr(field_info, "embed", None)
        value: Any = None

        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                values[field.name] = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
                
            if value is None or (isinstance(field_info, params.Form) and value == "") or \
                    (isinstance(field_info, params.Form) and field.shape in sequence_shapes and len(value) == 0):
                if field.required:
                    if PYDANTIC_1:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))
                else:
                    values[field.name] = deepcopy(field.default)
            elif isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                value = await value.read()
            elif field.shape in sequence_shapes and isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
                awaitables = [sub_value.read() for sub_value in value]
                contents = await asyncio.gather(*awaitables)
                values[field.name] = sequence_shape_to_type[field.shape](contents)
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

This corrected version ensures that each field in `required_params` is handled correctly based on its shape and type, with appropriate value extraction and validation for sequence shapes. The function should now correctly parse the received body and populate the values dictionary accordingly in line with the expected input/output values provided for the failing test cases.