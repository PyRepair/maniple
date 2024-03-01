### Analysis
1. The function `request_body_to_args` is designed to process required parameters and received body data. It iterates over the required fields, extracts values from the body data, handles file uploads, and validates the values against the field type.
2. The bug seems to stem from how the function handles sequence shapes (list, set, tuple) when processing form data.
3. In all failing cases, the function is not correctly handling the sequence shapes, leading to validation errors and returning a status code of 422 instead of 200.
4. To fix the bug, we need to ensure that the function correctly extracts and processes data for sequence-shaped fields (list, set, tuple) when dealing with form data.

### Bug Fix
Here is the corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
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
        elif isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
            if field.shape == 1:
                if isinstance(value, list):
                    values[field.name] = [await val.read() for val in value]
                else:
                    values[field.name] = await value.read()
            else:
                awaitables = [val.read() for val in value]
                contents = await asyncio.gather(*awaitables)
                values[field.name] = sequence_shape_to_type[field.shape](contents)
        else:
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

### Explanation
1. In the corrected version, the function now correctly handles sequence shapes when dealing with form data.
2. It checks if the field shape is a sequence shape and processes the data accordingly, ensuring proper handling of list, set, and tuple fields.
3. The function now properly validates the data, handles file uploads for sequence shapes, and constructs the response values accordingly.

By using this corrected version, the function should now correctly process the form data for sequence-shaped fields without throwing validation errors, and the failing tests should pass with this fix.