### Bug Explanation
The bug in the `request_body_to_args` function arises from the logic where it handles repeated keys in the FormData object. The function fails to correctly handle repeated keys when parsing FormData and does not aggregate them into a list as expected.

In the failing test cases, when the FormData contains multiple values for the same key, the function only considers the last value and does not treat them as a list or set depending on the field type specified.

The bug leads to validation errors and incorrect parsing of the input data in the case of repeated keys in the FormData.

### Bug Fix Strategy
To fix the bug in the `request_body_to_args` function, the handling of repeated keys in FormData needs to be adjusted. Rather than just using the last value, the function should aggregate all values for a repeated key into a list, set, or tuple based on the field type indicated.

### Updated Corrected Function
Here is the corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        if received_body is not None:
            for field in required_params:
                value: Any = None
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    values_list = received_body.getlist(field.alias)
                    if len(values_list) == 1:
                        value = values_list[0]
                    else:
                        if field.shape == 1:
                            value = values_list
                        elif field.shape == 2:
                            value = set(values_list)
                        elif field.shape == 3:
                            value = tuple(values_list)
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

                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
    return values, errors
```

This updated version modifies how the function processes repeated keys in FormData and correctly aggregates them into lists, sets, or tuples based on the field type. It should now handle the input correctly and pass the failing tests.