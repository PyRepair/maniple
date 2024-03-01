### Bug Analysis
1. The function `request_body_to_args` is designed to extract values from the received body based on the required parameters specified.
2. The bug appears to be related to handling repeated keys in form data when the `Form` parameters are of the `list`, `set`, or `tuple` types.

### Bug Explanation
The bug occurs when handling repeated keys in the form data for parameters like `list`, `set`, or `tuple`. The function does not aggregate the values correctly and only considers the last value for validation.

### Bug Fix Strategy
To fix this bug, we need to modify the function such that it aggregates repeated keys in the form data before validation. This can be achieved by checking for repeated keys during value extraction and organizing them into appropriate structures (`list`, `set`, or `tuple`) for validation.

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
                if isinstance(received_body, FormData):
                    if field.alias in received_body.keys():
                        field_values = received_body.getlist(field.alias)
                        if field.shape == 1:
                            value = field_values[0]  # For single value
                        elif field.shape == 2:
                            value = field_values  # For multiple values
            if value is None:
                if field.required:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                if isinstance(value, UploadFile):
                    value = await value.read()
                elif isinstance(value, list) and all(isinstance(v, UploadFile) for v in value):
                    awaitables = [sub_value.read() for sub_value in value]
                    contents = await asyncio.gather(*awaitables)
                    value = contents
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

This corrected version of the `request_body_to_args` function addresses the bug related to handling repeated keys in form data. It now correctly aggregates values for parameters like `list`, `set`, or `tuple` before validation, ensuring that all values are considered for validation.