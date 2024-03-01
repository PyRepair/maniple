### Analysis and Bug Explanation
The bug originates from the handling of repeated keys in the FormData when it contains multiple values for the same field. The current implementation only assigns the last value to the field, leading to validation issues. The bug is related to the GitHub issue titled "Support repeated key=value in form data".

### Bug Location
- The problematic section is where the received_body is being converted to key-value pairs and assigned to the values dictionary.
- The issue arises when there are multiple values for a single key in the FormData.

### Bug Cause
1. The bug lies in the conditional assignments of received_body values to the values dictionary. It does not handle multiple values for the same key correctly.
2. When a single key appears multiple times in FormData, only the last value is considered, leading to incorrect validation.

### Correction Strategy
To fix the bug and address the GitHub issue:
1. Update the logic to concatenate all values for the same key in a list.
2. Ensure that the values dictionary contains lists for entries with multiple values, addressing repeated key=value scenarios.
3. Properly process and validate all values for each key in the FormData.

### Corrected Function
Here is the corrected version of the function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        for field in required_params:
            value = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    values_list = received_body.getlist(field.alias)
                    if len(values_list) == 1:
                        value = values_list[0]
                    else:
                        value = values_list
                else:
                    value = received_body.get(field.alias)
            if (
                value is None
                or (isinstance(get_field_info(field), params.Form) and value == "")
                or (
                    isinstance(get_field_info(field), params.Form)
                    and field.shape in sequence_shapes
                    and len(value) == 0
                )
            ):
                if field.required:
                    if PYDANTIC_1:
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias))
                        )
                    else:  # pragma: nocover
                        errors.append(
                            ErrorWrapper(
                                MissingError(),
                                loc=("body", field.alias),
                                config=BaseConfig,
                            )
                        )
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

This corrected version should handle repeated keys correctly and resolve the validation issues related to the bug and the GitHub issue mentioned.