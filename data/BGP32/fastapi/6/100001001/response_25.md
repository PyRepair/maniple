The bug in the `request_body_to_args` function seems to stem from incorrectly handling sequence-shaped fields (like lists, sets, tuples) when parsing the `received_body`. Here's an explanation of the issue and suggested fix based on the provided runtime cases:

### Issue:
1. The function expects the `received_body` to be either a dictionary or FormData.
2. When dealing with sequence-shaped fields (e.g., lists, sets, tuples), the function fails to correctly extract the values from the `received_body`.
3. The handling of errors related to missing values or incorrect field types is not consistent and can lead to incorrect error reporting.

### Suggested Fix:
1. Correctly handle sequence-shaped fields when extracting values from `received_body`.
2. Ensure consistent and accurate error reporting for missing values or incorrect field types.

### Corrected Version of the Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params and (isinstance(received_body, dict) or isinstance(received_body, FormData)):
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
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
            if (
                isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
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

This corrected version should address the issues with handling sequence-shaped fields and ensure error reporting consistency. Test thoroughly to confirm that the function now behaves as expected and produces the correct output.