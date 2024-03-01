### Bug Explanation
The bug in the provided function arises from the handling of sequence-shaped fields (e.g., lists, sets, tuples) within the `received_body`. The function incorrectly processes these values, leading to errors and incorrect assignment of values to the `values` dictionary.

The bug occurs because the function assumes that `received_body` will always contain the entire list of values for a sequence-shaped field, which is not the case with FormData, where the values for a single key can be repeated. This assumption leads to errors in validation and value extraction.

### Bug Fix Strategy
To fix the bug, we need to modify how the function handles sequence-shaped fields within FormData. Instead of directly accessing the values in `received_body`, we should iterate over each key-value pair and accumulate the values for sequence-shaped fields to ensure correct extraction and validation.

### Corrected Function
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
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    values_list = []
                    for key, val in received_body.items():
                        if key == field.alias:
                            if field.shape == 1:
                                values_list.append(val)
                            else:
                                values_list.extend([item for item in val])
                    value = values_list
                else:
                    value = received_body.get(field.alias)
            if value is None or (isinstance(get_field_info(field), params.Form) and value == "") or (
                isinstance(get_field_info(field), params.Form) and field.shape in sequence_shapes and len(value) == 0
            ):
                if field.required:
                    if PYDANTIC_1:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:  # pragma: nocover
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            if isinstance(get_field_info(field), params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                value = await value.read()
            elif field.shape in sequence_shapes and isinstance(get_field_info(field), params.File) and lenient_issubclass(field.type_, bytes) and isinstance(
                value, sequence_types
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
                values[field.name] = v_
    return values, errors
```

This corrected version properly handles FormData inputs with sequence-shaped fields, ensuring correct value extraction and validation.