The bug in the provided function lies in the logic related to handling sequence shapes (like list, set, tuple) within received form data. When iterating over required parameters, the function incorrectly handles the sequence data and fails to populate the values correctly.

To fix the bug, we need to update the function to correctly handle sequence shapes and extract values based on the field's data type.

Here is the corrected version of the function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value = None
        if received_body is not None:
            value = received_body.get(field.alias)
            if value is None:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
                    continue
            if isinstance(field.type_, List) or isinstance(field.type_, Set) or isinstance(field.type_, Tuple):
                if isinstance(value, list) or isinstance(value, set) or isinstance(value, tuple):
                    v = value
                else:
                    v = [value]  # Convert non-sequence data to a list
            else:
                v = value
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(v, UploadFile):
                v = await v.read()
            v_, errors_ = field.validate(v, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

This corrected function iterates over each required parameter properly, fetches the value from the form data, and correctly processes sequence-shaped data if the field type suggests so. It handles different types of sequences (list, set, tuple) and processes the values accordingly.

Please test this corrected version with the failing cases provided to ensure that it now produces the expected results.