### Bug Explanation
The bug in the `request_body_to_args` function lies in how it handles sequences in the form data. When processing form data with multiple values for the same field (like a list, set, or tuple), the function incorrectly handles the extraction of these values from the FormData object.

The bug causes the function to fail when trying to extract values for fields that are supposed to hold lists, sets, or tuples, resulting in incorrectly processed data and potentially missing or incorrectly shaped output values.

### Bug Fix Strategy
To fix the bug, we need to properly handle the extraction of values for fields with sequence shapes from the FormData object. This involves correctly processing and validating the input data for these fields by considering and maintaining the sequence structure of the values.

### Corrected Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    for field in required_params:
        value = None
        
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.alias in received_body:
                    value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
            
        if value is None or (isinstance(field_info, params.Form) and value == "") or (
            isinstance(field_info, params.Form)
            and field.shape in sequence_shapes
            and len(value) == 0
        ):
            if field.required:
                if PYDANTIC_1:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if field.shape in sequence_shapes and isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                new_value = []
                for single_value in value:
                    if isinstance(single_value, UploadFile):
                        new_value.append(await single_value.read())
                value = new_value
            
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    
    return values, errors
```

By updating the logic for extracting and processing values from form data, the corrected function should now be able to handle sequence-shaped fields correctly and produce the expected output for the given test cases.