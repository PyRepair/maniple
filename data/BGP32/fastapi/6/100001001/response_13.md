### Bug Explanation
The bug in the `request_body_to_args` function occurs when handling sequences like lists, sets, and tuples in the input data. The function fails to correctly process sequence shapes, resulting in validation errors even when data is present.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function handles sequence shapes correctly and extracts the values from the input data in a proper manner, allowing validation to proceed without errors.

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
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            if value is None or value == "" or (field.shape in sequence_shapes and len(value) == 0):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
                    continue
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                value = await value.read()
            elif field.shape in sequence_shapes and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
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

### Changes Made
1. Removed the unnecessary conditions related to `field_info` and `embed` that were causing unnecessary complexity.
2. Simplified the check for missing or empty data in the received body.
3. Removed the redundant validation for cases where the field is not required.
4. Updated the logic for handling sequences to extract values correctly and validate them accordingly.