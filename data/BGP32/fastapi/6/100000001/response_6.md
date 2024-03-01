### Analysis:
1. The function `request_body_to_args` takes a list of required parameters along with a received body (either a dict or FormData).
2. It iterates over the required params and attempts to extract values from the received body based on the field aliases.
3. If a required field is missing in the received body, it adds a `MissingError` to the errors list.
4. The function handles cases for different types of fields such as `params.Form` and `params.File`.

### Potential Error Locations:
1. The `field_info` assignment may cause an error if `get_field_info` returns `None`.
2. The condition to check for empty value (`value == ""`) may not work as expected for non-string types.
3. There could be a potential issue in handling `await` calls within the loop.

### Bug Cause:
1. The loop logic for extracting values from the received body seems susceptible to errors when dealing with various types of fields.
2. There might be issues with the handling of missing or empty values leading to incorrect error generation or data extraction.

### Bug Fix Strategy:
1. Ensure that `field_info` is properly checked for `None` before accessing its attributes.
2. Improve the logic for handling empty values based on field types instead of relying on string comparison.
3. Investigate if the `await` calls are correctly structured within the loop.

### Corrected Version:
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
                field_info = get_field_info(field)
                if field_info is not None:
                    value = None
                    if field.shape in sequence_shapes and isinstance(received_body, FormData):
                        value = received_body.getlist(field.alias)
                    else:
                        value = received_body.get(field.alias)
                    if value is not None:
                        if isinstance(field_info, params.File) and \
                               lenient_issubclass(field.type_, bytes) and \
                               isinstance(value, UploadFile):
                            value = await value.read()
                        elif field.shape in sequence_shapes and \
                             isinstance(field_info, params.File) and \
                             lenient_issubclass(field.type_, bytes) and \
                             isinstance(value, sequence_types):
                            awaitables = [sub_value.read() for sub_value in value]
                            contents = await asyncio.gather(*awaitables)
                            value = sequence_shape_to_type[field.shape](contents)

                        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                        if isinstance(errors_, ErrorWrapper):
                            errors.append(errors_)
                        elif isinstance(errors_, list):
                            errors.extend(errors_)
                        else:
                            values[field.name] = v_
                    elif field.required:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    errors.append(ErrorWrapper(ValueError(f"Field info missing for: {field}"), loc=("body", field.alias)))

            else:
                errors.append(ErrorWrapper(ValueError(f"Received body is None for field: {field}"), loc=("body", field.alias)))

    return values, errors
```