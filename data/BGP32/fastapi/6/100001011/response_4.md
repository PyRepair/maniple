### Bug Explanation:
The issue arises due to the current implementation of `request_body_to_args` function not handling scenarios where multiple values with the same key are present in the `received_body` which causes only the last value to be considered. This behavior contradicts the expected behavior where all values should be considered and validated as a list when multiple values are present.

### Bug Fix Strategy:
To resolve the bug and align the behavior with the expectation mentioned in the GitHub issue, we need to modify the logic in the `request_body_to_args` function to handle cases where multiple values with the same key exist in the `received_body`. When multiple values are present, these values should be grouped and considered as a list for validation.

### Corrected Version of the Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        for field in required_params:
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    values[field.name] = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
                    if value is not None:
                        if field.shape in sequence_shapes and not isinstance(value, list):
                            values[field.name] = [value]
                        else:
                            values[field.name] = value
                    elif field.required:
                        if PYDANTIC_1:
                            errors.append(
                                ErrorWrapper(MissingError(), loc=("body", field.alias))
                            )
                        else:
                            errors.append(
                                ErrorWrapper(
                                    MissingError(), loc=("body", field.alias), config=BaseConfig
                                )
                            )
            elif field.required:
                if PYDANTIC_1:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig
                    )

    return values, errors
```

### Changes Made:
- Modified the logic where multiple values are now grouped as a list under the same key for validation.
- The function now correctly handles scenarios where multiple values with the same key exist in the `received_body` and processes them as expected.