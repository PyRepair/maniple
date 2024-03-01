### Bug Explanation
The bug in the `request_body_to_args` function is causing the response status code to be different from the expected status code in the provided tests. The function is not correctly handling the case where the input data is meant to be a sequence (list, set, tuple).

The issue arises from a specific condition check that attempts to handle a single field case without considering sequences. It fails to correctly process sequence data that arrives as a single value in the input. This results in the erroneous behavior where the data is not correctly extracted from the input data and formatted as a sequence in the output values.

### Bug Fix Strategy
To fix the bug, you need to modify the condition that handles the case for a single field without embed as it is currently affecting the correct extraction of sequence data. Additionally, the function needs to handle sequence data properly to ensure it is correctly extracted from the input data and formatted as the appropriate sequence type in the output values.

### Corrected Function
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
            if field.shape in sequence_shapes and isinstance(
                received_body, FormData
            ):
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
            
            if value is None or (isinstance(field_info, params.Form) and value == "") or (
                    isinstance(field_info, params.Form) and field.shape in sequence_shapes and len(value) == 0
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

            if field.shape in sequence_shapes:
                if field.type_ is list:
                    value = value
                elif field.type_ is set:
                    value = set(value)
                elif field.type_ is tuple:
                    value = tuple(value)
            
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

This corrected function ensures that it correctly handles sequence data input when extracting values and formatting them accordingly for further processing. It addresses the bug that caused the failing test cases by properly identifying and converting the sequence data within the input body to the corresponding sequence types in the output values.