### Analysis:
1. The function `request_body_to_args` is designed to extract values from a request body based on required parameters and handle different cases such as files, sequences, and form data.
2. The function loops through the required parameters, retrieves the corresponding values from the received body, performs validations, and populates the values dictionary or errors list accordingly.
3. The bug seems to stem from the handling of sequence shapes (list, set, tuple) when processing form data like FormData.
4. The incorrect handling of sequences and forms in the function is causing validation errors and incorrect value assignments.
5. We need to modify the logic related to sequence shapes and form handling to correctly extract and validate values from the request body.

### Bug Fix Strategy:
1. Update the logic for getting values from FormData for sequence shapes (list, set, tuple) to ensure correct extraction.
2. Correctly handle the validation and storing of values for each field.
3. Adjust the embed condition and provide appropriate values to the corresponding fields.
4. Implement specific validations for lists, sets, and tuples within FormData to prevent errors.
5. Modify the function to handle different sequence shapes and form data formats correctly.

### Corrected Version of the function `request_body_to_args`:
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
                    value = received_body.getlist(field.alias) if field.shape in sequence_shapes else received_body.get(field.alias)
                else:
                    value = received_body.get(field.alias)
            if value is None or (isinstance(field_info, params.Form) and value == "") or (isinstance(field_info, params.Form) and field.shape in sequence_shapes and len(value) == 0):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=('body', field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                value = await value.read()
            elif field.shape in sequence_shapes and isinstance(value, sequence_types):
                if all(isinstance(val, str) for val in value):
                    value = sequence_shape_to_type[field.shape](value)
                else:
                    awaitables = [sub_value.read() for sub_value in value]
                    contents = await asyncio.gather(*awaitables)
                    value = sequence_shape_to_type[field.shape](contents)
            v_, errors_ = field.validate(value, values, loc=('body', field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

By implementing the suggested changes and adjusting the logic related to sequence shapes and form data handling, the corrected function should now properly process the request body and pass the failing tests.