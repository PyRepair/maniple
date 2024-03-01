### Bug Explanation
The bug in the `request_body_to_args` function arises from how it handles sequences in the `received_body`. The function is intended to extract values from the `received_body` based on the required parameters. However, the current implementation fails to handle sequences properly, resulting in errors being generated.

### Bug Location
The issue lies in the handling of sequences (e.g., lists, sets, tuples) in the `received_body`. When iterating over the required parameters, the function incorrectly processes sequence shapes, leading to errors in validation and, ultimately, incorrect results.

### Bug Fix Strategy
To fix the bug, the function should be modified to correctly extract and process sequence values from the `received_body` while considering the sequence shapes specified in the required parameters.

### Corrected Version of the Function:
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
                value = received_body.getlist(field.alias) if field.shape == 1 else received_body.getlist(field.alias + "[]")
            else:
                value = received_body.get(field.alias)
        if value is None or (isinstance(field_info, params.Form) and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
            continue
        if (
            isinstance(field_info, params.File)
            and lenient_issubclass(field.type_, bytes)
            and isinstance(value, UploadFile)
        ):
            value = await value.read()
        if field.shape in sequence_shapes and isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
            if isinstance(value, sequence_types):
                awaitables = [item.read() for item in value]
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

This corrected version of the function properly handles sequences in the `received_body` and should resolve the issues related to incorrect validation and error generation.