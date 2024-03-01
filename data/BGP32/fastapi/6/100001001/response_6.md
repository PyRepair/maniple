### Explanation

The bug in the function `request_body_to_args` arises from the incorrect handling of fields with `sequence_shapes` when the received body is a `FormData`. The function is designed to extract values from the received body based on the provided required parameters. However, the logic dealing with sequences like lists, sets, and tuples when processing FormData is flawed. It fails to properly extract values and validate them against the required parameters, leading to errors.

### Bug Fix Strategy

1. Update the logic for handling sequence shapes when the received body is a `FormData`.
2. Ensure that values extracted from the FormData are correctly processed and validated against the required parameters.
3. Resolve the errors for missing values and mismatched types.

### Corrected Version

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
                value = received_body.get(field.alias)
                if value is None:
                    if field.required:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:
                        values[field.name] = deepcopy(field.default)
                    continue
                if field.shape in sequence_shapes and isinstance(
                    value, FormData
                ):
                    if field.type_ == list:
                        value = value.getlist(field.alias)
                    elif field.type_ == set:
                        value = set(value.getlist(field.alias))
                    elif field.type_ == tuple:
                        value = tuple(value.getlist(field.alias))
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
                    values[field.name] = v_
    return values, errors
```

In the corrected version:
- Extract values from the FormData based on the field's type and handle lists, sets, and tuples appropriately.
- Validate values against the required parameters and handle missing values according to the field's requirements.
- Ensure proper processing and validation of values extracted from FormData based on the field specifications.