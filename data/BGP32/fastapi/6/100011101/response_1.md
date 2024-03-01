### Bug Explanation
The bug in the `request_body_to_args` function is due to the handling of non-typing sequence shapes (list, set, tuple) when parsing the received body. The function fails to correctly convert these non-typing sequences from the `received_body` into the expected data types (list, set, tuple) for the specified field.

### Bug Fix Strategy
To fix the bug, we need to modify the function to correctly handle non-typing sequences in the received body. Each non-typing sequence should be converted accordingly to match the expected type of the field.

### Corrected Version of the Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        field = required_params[0]
        field_info = get_field_info(field)
        embed = getattr(field_info, "embed", None)
        if len(required_params) == 1 and not embed:
            received_body = {field.alias: received_body}
        for field in required_params:
            value: Any = None
            if received_body is not None:
                value = received_body.getlist(field.alias) if field.shape in sequence_shapes and isinstance(received_body, FormData) else received_body.get(field.alias)

            if value is None or value == "":
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
                continue

            if field.shape in sequence_shapes:
                if lenient_issubclass(field.type_, list):
                    value = value
                elif lenient_issubclass(field.type_, set):
                    value = set(value)
                elif lenient_issubclass(field.type_, tuple):
                    value = tuple(value)

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

By incorporating the correct handling of non-typing sequences in the received body and converting them to the expected data types, the corrected version of the function should now pass the failing tests and satisfy the expected input/output values provided.