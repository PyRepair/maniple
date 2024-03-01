The bug in the `request_body_to_args` function lies in how the values are extracted from the `received_body` based on the field's shape. The current implementation does not handle sequences properly, leading to incorrect validation and errors during the tests.

To fix the bug:
1. Modify the logic for extracting values from `received_body` for sequence shapes (list, set, tuple) to handle them correctly.
2. Update the validation process to address sequence values properly.
3. Update the construction of the `values` dictionary with the correct values extracted from `received_body`.

Here is the corrected version of the function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        for field in required_params:
            value = None
            if received_body is not None:
                field_info = get_field_info(field)
                
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    value = received_body.getlist(field.alias)
                    if field_info.sub_fields:
                        sub_values = []
                        for sub_value in value:
                            sub_values.append(field_info.fields[0].sub_fields[0].validate(sub_value, {}, loc=('body', field.alias))[0])
                        value = sub_values
                else:
                    value = received_body.get(field.alias)
                
            if value is None:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if field.shape in sequence_shapes:
                    if not isinstance(value, sequence_types):
                        errors.append(ErrorWrapper(ValidationError(), loc=("body", field.alias)))
                    else:
                        values[field.name] = value
                else:
                    if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                        value = await value.read()
                    v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                    if isinstance(errors_, ErrorWrapper): errors.append(errors_)
                    elif isinstance(errors_, list): errors.extend(errors_)
                    else: values[field.name] = v_
                
    return values, errors
```

By incorporating the corrections mentioned above, the function should now handle lists, sets, and tuples correctly when extracting values from `received_body`. This should address the errors during the failing tests and align with the expected results.