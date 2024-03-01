### Bug Analysis

#### Potential Error Locations
1. The handling of `field.shape in sequence_shapes` might be causing issues with form data processing for non-typing sequences like lists, sets, and tuples.
2. Incorrect assignment of `received_body` when there is only one `required_param` and no `embed`.
3. Issues with validation and error reporting for non-typing sequences.

#### Bug Cause
The bug is likely caused by the mishandling of the form data for non-typing sequences like lists, sets, and tuples in the `request_body_to_args` function. When processing form data for such sequences, the function encounters issues with data extraction, validation, and error reporting due to incorrect condition checks and assignments.

#### Bug Fix Strategy
1. Ensure correct extraction and processing of form data for different non-typing sequences.
2. Fix any issues related to data validation and error generation for sequences.

### Corrected Version of the Function

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        if len(required_params) == 1 and not getattr(get_field_info(required_params[0]), "embed", None):
            received_body = {required_params[0].alias: received_body}
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    if field.alias in received_body.keys():
                        value = received_body.getlist(field.alias)
                    else:
                        value = received_body.get(field.alias)
            if value is None or (isinstance(get_field_info(field), params.Form) and value == "") or (
                isinstance(get_field_info(field), params.Form) and field.shape in sequence_shapes and len(value) == 0
            ):
                if field.required:
                    if PYDANTIC_1:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            if (
                isinstance(get_field_info(field), params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif (
                field.shape in sequence_shapes
                and isinstance(get_field_info(field), params.File)
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

By updating the function with corrections to handle form data for non-typing sequences properly and ensuring correct validation and error handling, the corrected version should now pass the failing tests and resolve the GitHub issue related to supporting repeated key=value pairs in form data.