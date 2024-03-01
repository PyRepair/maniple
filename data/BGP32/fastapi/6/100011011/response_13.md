### Bug Analysis
1. The bug is related to the handling of repeated keys in form data. The request_body_to_args function does not account for repeated keys when processing FormData, leading to only the last key=value pair being considered.
2. The function is expected to extract values from the received_body FormData based on the required_params list of ModelFields.
3. The bug causes the function to miss processing all values if the same key appears multiple times in the FormData. This results in validation errors as observed in the failing tests.
4. To fix the bug, the function needs to be modified to handle repeated keys properly and extract all corresponding values for validation.

### Bug Fix Strategy
To address the bug and support repeated key=value pairs in form data:
1. Modify the logic to check for repeated keys and accumulate all associated values before processing.
2. Update the assignment of values based on keys to handle multiple values by converting them to lists.
3. Ensure that the validation logic accounts for these changes to handle multiple values when validating.

### Bug-Fixed Version
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if received_body:
        data = received_body.items() if isinstance(received_body, dict) else received_body
        processed_values = {}
        for key, value in data:
            if key in processed_values:
                processed_values[key].append(value)
            else:
                processed_values[key] = [value]

        for field in required_params:
            value = processed_values.get(field.alias)
            if not value:
                if field.required:
                    if PYDANTIC_1:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))
                else:
                    values[field.name] = deepcopy(field.default)
                continue

            if len(value) == 1:
                value = value[0]

            if (
                isinstance(field.field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif (
                field.shape in sequence_shapes
                and isinstance(field.field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, sequence_types)
            ):
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

    return values, errors
```

By updating the function to properly handle repeated keys and process all associated values, the bug should be resolved, and the failing tests related to form data with repeated keys should pass.