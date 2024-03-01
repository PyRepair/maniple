## Bug Explanation:

The buggy function `request_body_to_args` has a problem when processing form data with repeated keys. In the failing tests provided:
- `test_python_list_param_as_form`: A list parameter is expected, but only the last value is retained due to how the function processes the data.
- `test_python_set_param_as_form`: A set parameter is expected, but the same issue occurs where only the last value is kept.
- `test_python_tuple_param_as_form`: A tuple parameter is expected, but again, only the last value is considered.

The issue arises from the way the function handles data with repeated keys in FormData. It only retains the last value instead of collecting all values into a list, set, or tuple based on the parameter's type.

## Fix Strategy:

To fix the bug, we need to modify the function to correctly handle repeated keys and collect all values into the appropriate data structure (list, set, or tuple) based on the type of the parameter.

## Corrected Version of the Function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    for field in required_params:
        value: Any = None
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.alias in received_body:
                    if field.shape == 3:
                        value = tuple(received_body.getlist(field.alias))
                    elif field.shape == 4:
                        value = set(received_body.getlist(field.alias))
                    else:
                        value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
        
        if (
            value is None
            or (isinstance(field_info, params.Form) and value == "")
            or (
                isinstance(field_info, params.Form)
                and field.shape in sequence_shapes
                and len(value) == 0
            )
        ):
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

By modifying the function as shown above, the corrected version should be able to handle form data with repeated keys correctly and collect all values into the appropriate data structure based on the parameter's type, addressing the bug reported in the GitHub issue.