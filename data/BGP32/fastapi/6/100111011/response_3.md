### Bug Analysis
1. The `request_body_to_args` function is responsible for extracting values from the received body based on required parameters.
2. The function seems to have an issue when dealing with sequence shapes like list, set, tuple in the received body.
3. The function attempts to get the values from the received body based on the field alias, but there seem to be issues with appending these values correctly.
4. The failing tests are due to the incorrect assignment of values from received body to the expected parameters.
5. The error messages indicate that the status codes are not as expected due to validation errors.
6. The GitHub issue relates to the handling of repeated key=value pairs in form data, which could impact the correct extraction of values in the function.

### Bug Fix Strategy
1. Update the function to correctly handle repeated key=value pairs in form data.
2. Ensure that when multiple values are provided for the same key, they are collected in a list and assigned appropriately.
3. Debug the function to ensure that the values are correctly extracted based on the field alias.
4. Implement changes to address the bug and make sure that repeated key=value pairs are collected and validated correctly.

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
                    if field.alias in received_body and hasattr(received_body[field.alias], 'append'):
                        value = received_body[field.alias]
                    else:
                        value = [received_body.get(field.alias)]
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

In the corrected version, extra logic has been added to correctly handle sequence shapes in the received body data, ensuring that multiple values for the same key are collected and processed appropriately. This fix should address the issues encountered in the failing tests and also align with the suggested changes in the related GitHub issue.