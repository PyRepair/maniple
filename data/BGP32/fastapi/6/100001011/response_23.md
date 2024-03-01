The bug in the `request_body_to_args` function stems from the handling of repeated keys in form data. The provided function fails to correctly handle repeated keys and only considers the last value in the keys list. This behavior does not align with the expected functionality, especially when dealing with form data containing repeated keys that should be processed as a list.

To address this issue, we need to update the function to appropriately handle repeated keys in form data by aggregating them into a list before validation. A revised version of the function is presented below to resolve the problem:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        values[field.name] = None
        if received_body is not None:
            if field.alias in received_body:
                if isinstance(received_body, FormData):
                    values[field.name] = received_body.getlist(field.alias)
                else:
                    values[field.name] = received_body.get(field.alias)
        if values[field.name] is None:
            if field.required:
                errors.append(
                    ErrorWrapper(MissingError(), loc=("body", field.alias))
                )
            else:
                values[field.name] = deepcopy(field.default)
            continue

        if isinstance(field.type_, (list, set, tuple)) and not isinstance(values[field.name], (list, set, tuple)):
            values[field.name] = [values[field.name]]

        value = values[field.name]
        if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
            if isinstance(value, list):
                awaitables = [sub_value.read() for sub_value in value]
                contents = await asyncio.gather(*awaitables)
                values[field.name] = sequence_shape_to_type[field.shape](contents)
            else:
                values[field.name] = await value.read()

        v_, errors_ = field.validate(values[field.name], values, loc=("body", field.alias))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_

    return values, errors
```

In this corrected version, repeated keys in form data are gathered into a list before validation. This ensures that all values associated with a particular key are considered during validation. This modification addresses the GitHub issue's request for support for repeated key=value pairs in form data.