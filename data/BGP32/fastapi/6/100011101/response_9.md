## Bug Explanation
The bug lies in how the function `request_body_to_args` handles the different types of sequences (list, set, tuple) when processing the received body data. The function incorrectly processes these sequence types, leading to validation errors and status code 422 (Unprocessable Entity) instead of the expected 200 status code.

### Issues:
1. The function doesn't properly handle the conversion of the received body data into the desired sequence type (list, set, tuple).
2. The function misses the appropriate data types when constructing the final `values` dictionary.

### Strategy for Fixing the Bug
1. Correctly convert the received body data to the desired target sequence type.
2. Update the data types of the values stored in the `values` dictionary to match the expected sequence type.

## Corrected Function
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
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    if field.shape == 2:  # handle set
                        value = set(received_body.getlist(field.alias))
                    elif field.shape == 3:  # handle tuple
                        value = tuple(received_body.getlist(field.alias))
                    else:  # handle list
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
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            if (
                isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif (
                field.shape in sequence_shapes
                and isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, sequence_types)
            ):
                awaitables = [sub_value.read() for sub_value in value]
                contents = await asyncio.gather(*awaitables)
                value = sequence_shape_to_type[field.shape](contents)
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.alias if embed else field.name] = v_
    return values, errors
```

By updating the handling of different sequence shapes (list, set, tuple) in the `request_body_to_args` function, the corrected version should be able to process the received body correctly and return the expected values, thus passing the failing tests.