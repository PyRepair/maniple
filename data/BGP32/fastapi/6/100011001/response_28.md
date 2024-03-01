### Bug Analysis
- The bug occurs because the function is not handling the case where the received body contains multiple values for the same field, which happens when the field is part of a non-typing sequence like a list, set, or tuple.
- The function fails to correctly extract values from FormData in these cases, leading to validation errors and ultimately the 422 status code in the tests.

### Bug Fix Strategy
1. When the received body is a FormData and the field is part of a sequence shape, the function should ensure to extract all values associated with that field.
2. For non-typing sequence fields, each value should be processed individually before any validation is carried out.

### Corrected Version of the Function

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
                if (
                    field.shape in sequence_shapes
                    and isinstance(received_body, FormData)
                    and field.alias in received_body
                ):
                    if isinstance(received_body[field.alias], list):
                        value = received_body.getlist(field.alias)
                    else:
                        value = [received_body[field.alias]]

            for item_value in value:
                if (
                    item_value is None
                    or (isinstance(field_info, params.Form) and item_value == "")
                    or (
                        isinstance(field_info, params.Form)
                        and field.shape in sequence_shapes
                        and len(item_value) == 0
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
                    and isinstance(item_value, UploadFile)
                ):
                    item_value = await item_value.read()

                v_, errors_ = field.validate(
                    item_value, values, loc=("body", field.alias)
                )
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)

                values.setdefault(field.name, []).append(v_)

    return values, errors
```

### Changes Made
1. Added logic to handle multiple values for a field in a non-typing sequence.
2. Process each value separately for validation.
3. Updated the value assignment logic based on the type of sequence.