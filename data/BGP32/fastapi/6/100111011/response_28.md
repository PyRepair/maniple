### Bug Analysis:
- The function `request_body_to_args` is responsible for converting request body data into arguments for the FastAPI route function to process.
- The function identifies the fields to extract from the received body and then validates and processes them accordingly.
- The bug seems to be related to processing sequences (like lists, sets, tuples) within the request body.
- In the provided test cases, the function is failing to properly handle the sequence data passed in the form.
- The failing tests are receiving a status code of 422 (Unprocessable Entity) instead of the expected 200.

### Error Cause:
- The bug occurs when handling sequences (list, set, tuple) within the `received_body` while extracting data based on field aliases.
- The function does not handle processing sequences correctly, leading to validation errors and returning incorrect status codes.
- The issue reported on GitHub also suggests the need to support repeated keys in form data, which relates to the bug in handling sequences as repeated values in the form data.
- The bug prevents proper validation of sequences from the form data, resulting in the test failures.

### Bug Fix Strategy:
To fix the bug and address the failing tests:
1. Update how sequences are processed in the `received_body` by extracting them based on field aliases and handle them appropriately.
2. Ensure that sequences are correctly validated and processed to align with the expected behavior of the route function.
3. Modify the function logic related to processing sequences to account for repeated keys in the form data as requested in the GitHub issue.

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
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    if field.alias in received_body.keys():
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
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
                if field.shape in sequence_shapes:
                    contents = []
                    for sub_value in value:
                        if isinstance(sub_value, UploadFile):
                            contents.append(await sub_value.read())
                    value = sequence_shape_to_type[field.shape](contents)
                else:
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

This corrected version of the function includes changes to properly handle sequences in the received form data, validate them, and ensure the route function processes them correctly. By addressing the sequence processing issues, the function should now pass the failing tests and align with the expected behavior based on the provided GitHub issue.