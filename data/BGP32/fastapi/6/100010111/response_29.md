### Bug Explanation
The buggy function `request_body_to_args` is intended to convert received body data into arguments compliant with the required parameters. However, the bug occurs when iterating over the required parameters to handle cases where the shape is a sequence (like a list, set, or tuple). The function incorrectly handles these cases due to the way it extracts values from the received body, leading to validation issues and ultimately causing the test failures.

The bug arises from incorrect handling when the field's shape is a sequence and the received body is of type `FormData`. In these cases, the function fails to correctly extract the values associated with the field alias, leading to incorrect results during validation. This issue aligns with the GitHub problem statement, indicating that values like repeated keys in form data are not being handled correctly.

### Bug Fix Strategy
To address this bug and align the function with the expected behavior and GitHub issue, the following steps can be taken:
1. Ensure that when iterating over required parameters, values from the received body are correctly extracted based on the field's shape and type.
2. Specifically handle the situation where the field's shape is a sequence (list, set, tuple) and the received body is a `FormData`, extracting the appropriate values as expected.
3. Implement the necessary changes to correctly handle repeated keys in form data, converting them into a list under the same key before validation.

### Corrected Function
Below is the corrected version of the function `request_body_to_args` that addresses the identified bug and aligns with the expected input/output values and the GitHub issue:

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
                        if field.shape == 1:
                            value = received_body.getlist(field.alias)
                        elif field.shape == 2:
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
                    else:  # pragma: nocover
                        errors.append(
                            ErrorWrapper(  # type: ignore
                                MissingError(),
                                loc=("body", field.alias),
                                config=BaseConfig,
                            )
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

With these corrections, the function should now handle sequence shapes like lists, sets, and tuples correctly when receiving data from `FormData`. Additionally, it aligns with the expected input/output values and addresses the issue raised on GitHub regarding support for repeated keys in form data.