### Explanation:
The buggy function `request_body_to_args` is supposed to convert the received body data into arguments based on the required parameters provided. The function iterates through the required parameters, extracts the corresponding values from the received body, validates them, and then populates the values dict while collecting any errors encountered.

The bugs in the function arise from how it handles different types of fields and shapes within the received body data. It fails to correctly process fields with different shapes (e.g., sequences like lists, sets, tuples) resulting in validation errors and incorrect values.

### Bug Fix Strategy:
To address the bugs in the function, we need to ensure that it correctly handles sequential shapes (lists, sets, tuples) within the received body data. This involves correctly retrieving, parsing, and validating these values according to the field's specifications.

### Fixed Version of the Function:
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
            field_name = field.alias
            value = None

            if received_body is not None:
                if isinstance(field_info, params.Form):
                    if field.shape in sequence_shapes and isinstance(received_body, FormData):
                        raw_values = received_body.getlist(field_name)

                        if field.shape in sequence_shapes:
                            parsed_values = []
                            for val in raw_values:
                                parsed_value, sub_errors = field.validate(val, values, loc=("body", field_name))
                                if isinstance(sub_errors, ErrorWrapper):
                                    errors.append(sub_errors)
                                elif isinstance(sub_errors, list):
                                    errors.extend(sub_errors)
                                parsed_values.append(parsed_value)

                            value = sequence_shape_to_type[field.shape](parsed_values)
                        else:
                            value = received_body.get(field_name)
                    else:
                        value = received_body.get(field_name)

            if value is None or (isinstance(field_info, params.Form) and value == ""):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field_name))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                    if isinstance(value, UploadFile):
                        value = await value.read()

                v_, errors_ = field.validate(value, values, loc=("body", field_name))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
                
    return values, errors
```

This corrected version handles the different shapes of fields correctly, parsing and validating the values within these fields based on their specifications. It should address the issues observed in the failing test cases.