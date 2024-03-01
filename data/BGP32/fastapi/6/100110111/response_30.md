### Analysis
1. The `request_body_to_args` function is responsible for extracting values from request bodies based on required parameters passed to it.
2. The function is currently not handling repeated keys in form data properly, which is causing the failing tests.
3. The bug appears to be related to how the function processes repeated keys in the form data and assigns values to them.
4. The expected input/output variable values provided in the test cases show the correct behavior that the function should exhibit.
5. The GitHub issue suggests that FastAPI should collect repeated keys in form data and assign those values as a list to the same key before validation.

### Bug Cause
The bug arises from the processing of form data with repeated keys. The function currently only considers the last key=value pair and does not handle multiple values for the same key correctly. This leads to incorrect validation and results in the failing tests.

### Bug Fix Strategy
To fix the bug, the function needs to correctly handle repeated keys in form data and assign the values as a list to the same key before validation. This aligns with the desired behavior mentioned in the GitHub issue.

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
            values[field.name] = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    values[field.name] = received_body.getlist(field.alias)
                else:
                    values[field.name] = received_body.get(field.alias)
            if values[field.name] is None or (
                isinstance(get_field_info(field), params.Form)
                and isinstance(values[field.name], str)
                and not values[field.name]
            ):
                if field.required:
                    if PYDANTIC_1:
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias))
                        )
                    else:  # pragma: nocover
                        errors.append(
                            ErrorWrapper(
                                MissingError(), loc=("body", field.alias), config=BaseConfig
                            )
                        )
                else:
                    values[field.name] = deepcopy(field.default)
    return values, errors
```

### Explanation
1. The corrected function iterates through each required parameter, correctly assigns values to keys from form data, and handles repeated keys by mapping them to a list.
2. It checks for missing or empty values based on the type of field and updates the `values` dictionary accordingly.
3. The function now aligns with the expected behavior in the failing test cases and GitHub issue.
4. The corrected function should now properly extract values from form data and handle repeated keys, resolving the bug and passing the failing tests.