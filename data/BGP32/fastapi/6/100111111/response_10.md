The bug in the `request_body_to_args` function is causing the failing test cases due to how repeated keys in FormData are handled. The function incorrectly assumes that only the last key=value pair is received, leading to validation errors. To fix this bug, we need to modify the logic to handle multiple values for a single key properly.

Here's an updated version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    if field.alias in received_body:
                        value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)

            if field.required and (value is None or value == "" or len(value) == 0):
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
            elif value is not None:
                if field.shape in sequence_shapes:
                    if isinstance(value, list):
                        v_list = []
                        for v in value:
                            if isinstance(v, UploadFile):
                                v_list.append(await v.read())
                            else:
                                v_list.append(v)
                        v_ = v_list
                    else:
                        v_ = value
                elif isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                    v_ = await value.read()
                else:
                    v_ = value

                v_, errors_ = field.validate(v_, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)

                values[field.name] = v_

    return values, errors
```

In this updated version, we correctly handle multiple values for the same key in FormData. We check if the field alias is present in the FormData and get all values associated with that key using `getlist` for lists. This change ensures that all values for a specific key are considered for validation.

With this correction, the `request_body_to_args` function should now handle repeated keys in FormData correctly and pass the failing tests with the expected input/output values.