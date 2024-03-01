### Analysis:
The `request_body_to_args` function is designed to extract values from the received body data based on the required parameters defined in the `required_params` list. It handles different data types like FormData, UploadFile, etc., and validates the received values against the required parameters.

### Identified Potential Errors:
1. In the line `field = required_params[0]`, the function assumes that the first element in `required_params` is the only field being processed. This might lead to incorrect behavior if multiple fields are present.
2. The check for `embed` attribute might not work as intended due to the logic in the subsequent lines.
3. There is a possibility of issues in handling sequence types like FormData and validating against the required fields.
4. Error handling for missing values or empty strings might not work correctly.

### Bug Explanation:
The bug arises from the assumption that only the first field in `required_params` needs to be processed, which might not be true for cases where multiple fields are involved. This can lead to missing or incorrect validation of the required fields.

### Bug Fix Strategy:
1. Iterate over all the fields in `required_params` to ensure all fields are processed correctly.
2. Make sure the logic for handling different shapes and data types is consistent and covers all edge cases.
3. Enhance error handling to effectively identify missing values and handle empty strings appropriately.

### Bug-free Corrected Version:
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
        if len(required_params) == 1 and not embed:
            received_body = {field.alias: received_body}
        
        value: Any = None
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(
                received_body, FormData
            ):
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
        
        if value is None or (isinstance(field_info, params.Form) and value == "") or (isinstance(field_info, params.Form) and field.shape in sequence_shapes and len(value) == 0):
            if field.required:
                if PYDANTIC_1:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:  
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))
            else:
                values[field.name] = deepcopy(field.default)
            continue
        
        if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
            value = await value.read()
        elif field.shape in sequence_shapes and isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
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

### Summary:
The corrected version of the `request_body_to_args` function addresses the identified potential errors and implements a more robust processing of the required parameters. Now, the function iterates over all the fields in `required_params` and handles different data types and shapes more effectively for accurate validation and extraction of values from the received body data.