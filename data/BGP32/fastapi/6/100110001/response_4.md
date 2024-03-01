### Analysis:
1. The `request_body_to_args` function is designed to convert received data into arguments based on required parameters.
2. The failing tests are related to submitting data for Python list, set, and tuple parameters in form data.
3. The error message indicates that the response status code is 422 (unprocessable entity) instead of the expected 200 (OK).
4. The bug seems to be related to how the function handles sequence-shaped parameters, causing validation errors and returning the wrong response status code.
5. We need to adjust the handling of sequence-shaped parameters in the function to correctly process and validate the input.

### Bug Cause:
- The bug occurs when the function encounters a sequence-shaped parameter (list, set, tuple) in the received form data. It fails to correctly process and validate such parameters leading to validation errors and incorrect response status codes.

### Bug Fix Strategy:
- Update the function logic to handle sequence-shaped parameters in the form data correctly.
- Ensure that sequence-shaped parameters are converted to the desired Python data structure and validated appropriately.

### The corrected version of the `request_body_to_args` function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    sequence_shapes = ["list", "set", "tuple"]
    for field in required_params:
        value: Any = None
        if received_body is not None:
            if field.shape in sequence_shapes:
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
        if value is None:
            if field.required:
                errors.append(
                    ErrorWrapper(MissingError(), loc=("body", field.alias))
                )
            else:
                values[field.name] = deepcopy(field.default)
            continue
        if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
            awaitables = [sub_value.read() for sub_value in value]
            contents = await asyncio.gather(*awaitables)
            data = sequence_shape_to_type[field.shape](contents)
            v_, errors_ = field.validate(data, values, loc=("body", field.alias))
        else:
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                value = await value.read()
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_
    return values, errors
```

After applying the above corrections, the `request_body_to_args` function should now be able to correctly handle sequence-shaped parameters in the form data and pass the failing tests.