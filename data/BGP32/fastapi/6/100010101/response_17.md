### Bug Explanation
The bug occurs because the function `request_body_to_args` is not handling non-typing sequences (`list`, `set`, `tuple`) correctly when the input is received as `FormData`. The function is designed to extract values from the `received_body` based on the specified `required_params` which are instances of `ModelField`. However, for non-typing sequence fields, the function is trying to extract a single value instead of a collection of values. This leads to incorrect validation and subsequently returns a status code of `422` instead of the expected `200`.

### Bug Fix Strategy
To fix the bug, we need to modify the logic for extracting values from `received_body` for non-typing sequences (`list`, `set`, `tuple`). Specifically, we need to handle such fields differently to capture the values correctly in a collection rather than as individual items while considering the `shape` of the field.


### Corrected Version of the Function
Here is the corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        for field in required_params:
            field_info = get_field_info(field)
            embed = getattr(field_info, "embed", None)
            if len(required_params) == 1 and not embed:
                received_body = {field.alias: received_body}
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    value = received_body.getlist(field.alias) if field.shape == 1 else received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            if (
                value is None
                or (isinstance(field_info, params.Form) and value == "")
                or (
                    isinstance(field_info, params.Form)
                    and field.shape in sequence_shapes
                    and len(value) == 0
                )
            ):
                if field.required:
                    if PYDANTIC_1:
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias))
                        )
                    else:
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig)
                        )
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            if (
                isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif (
                field.shape in sequence_shapes
                and isinstance(field_info, params.File)
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

### Additional Notes
1. Make sure to replace the existing `request_body_to_args` function with the corrected version in the appropriate file.
2. Running the failing tests after applying the corrected version should result in passing status codes (200) as per the expected values.