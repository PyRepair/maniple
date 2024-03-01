The bug in the `request_body_to_args` function is related to handling multiple values for the same key in the `FormData`. The function is not correctly converting these multiple values into the expected format.

### Bug Explanation:
When multiple values are provided for the same key in the `FormData`, the function only considers the last value instead of aggregating all values into a list, set, or tuple based on the field type. This behavior contradicts the expected functionality, as described in the GitHub issue, where multiple values for the same key should be collected and validated as a list.

### Bug Fix Strategy:
1. Identify the keys with multiple values in the `FormData`.
2. Aggregate these multiple values according to the field type (list, set, tuple).
3. Update the `values` dictionary accordingly.
4. Ensure error handling is consistent and accurate.

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
                values_list = received_body.getlist(field.alias)
                if field.shape == 1:
                    value = values_list
                elif field.shape == 2:
                    value = set(values_list)
                elif field.shape == 3:
                    value = tuple(values_list)
            else:
                value = received_body.get(field.alias)
        
        if value is None or (
            isinstance(field_info, params.Form)
            and isinstance(value, str)
            and value == ""
        ):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
            else:
                values[field.name] = deepcopy(field.default)
            continue

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

In this corrected version of the function, I have modified the logic to handle multiple values for the same key in `FormData` correctly based on the field shape. The function now aggregates the values into a list, set, or tuple accordingly. This modification aligns with the expectations outlined in the GitHub issue.

This corrected function should now handle the input scenarios as described in the expected cases and address the reported issue effectively.