### Analysis:
1. The `request_body_to_args` function is responsible for extracting values from the received body based on the required parameters provided. It seems to handle sequences differently based on whether the shape of the field is in `sequence_shapes`.
2. The failing tests are checking the response status code against 200, but the actual response status code is 422.
3. The error message indicates that the response status code is 422 instead of 200, leading to assertion errors in the tests.
4. The bug may be related to how the function handles sequence shapes and how it extracts values from a received form data when the field shape is in `sequence_shapes`.
5. To fix the bug, we need to ensure that the function correctly extracts and processes values from form data for sequence-shaped fields.

### Bug Fix Strategy:
1. Inspect how sequence-shaped fields are handled in the function.
2. Identify the issue related to handling form data for sequence-shaped fields.
3. Make necessary adjustments to correctly extract values for sequence-shaped fields.
4. Ensure the function correctly populates the `values` and `errors` lists.
5. Update the function to return the correct values and process form data appropriately.

### Corrected Version
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value: Any = None
        field_info = get_field_info(field)
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.shape in sequence_shapes:
                    values[field.alias] = received_body.getlist(field.alias)
                else:
                    values[field.alias] = received_body.getlist(field.alias)[0]
            else:
                values[field.alias] = received_body.get(field.alias) if received_body.get(field.alias) else None

        if values[field.alias] is None and field.required:
            if PYDANTIC_1:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                errors.append(
                    ErrorWrapper(
                        MissingError(),
                        loc=("body", field.alias),
                        config=BaseConfig,
                    )
                )
        else:
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                value = await values[field.alias].read()
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

This corrected version should address the issue with handling sequence-shaped fields in the function `request_body_to_args` and ensure that the values are correctly extracted from the form data. This should resolve the failing tests by returning the expected values for the provided data.