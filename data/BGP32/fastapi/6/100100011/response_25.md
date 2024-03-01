### Analysis:
The `request_body_to_args` function appears to be handling the conversion of request body data into Python arguments for FastAPI endpoints. The issue seems to be related to processing sequences in form data.

### Identified Bug:
The bug seems to be related to how the function is handling sequences in form data. In particular, when dealing with instances of `FormData` and processing sequence values, the function may not be handling them correctly.

### Cause of the Bug:
The bug seems to stem from how the function processes sequences in form data. This can be seen in the failing test cases where lists, sets, and tuples are being sent as form data, which the function is failing to handle correctly, leading to incorrect values or errors.

### Fix Strategy:
To fix the bug, we need to ensure that the function correctly handles sequences in form data, such as lists, sets, and tuples. This involves properly extracting sequence values from the form data and processing them accordingly.

### Corrected Version of the Function:
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
                if field.alias in received_body:
                    value = received_body.get(field.alias)
        
        if value is None or (isinstance(get_field_info(field), params.Form) and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
            elif field.default is not None:
                values[field.name] = deepcopy(field.default)
        else:
            if field.shape in sequence_shapes:
                if isinstance(value, sequence_types):
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
The corrected version of the `request_body_to_args` function should now correctly handle sequences in form data, ensuring that values are extracted and processed appropriately. This should resolve the issue reported on GitHub and allow the function to pass the failing test cases provided.