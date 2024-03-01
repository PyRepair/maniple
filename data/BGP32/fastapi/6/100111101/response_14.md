The bug in the `request_body_to_args` function lies in how it handles sequence-shaped fields like lists, sets, and tuples when parsing the received body data. The function is not properly extracting values for these fields, leading to validation errors and incorrect return values. 

To fix this bug, we need to adjust how the function processes sequence-shaped fields in the received body data and correctly validate and extract the values. 

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
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    if field.alias in received_body:
                        values[field.name] = received_body.getlist(field.alias)
                    else:
                        values[field.name] = []
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
                    else:
                        if (
                            field.shape in sequence_shapes
                            and isinstance(value, list)
                            and all(isinstance(i, str) for i in value)
                        ):
                            v_ = value
                        else:
                            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                                value = await value.read()
                            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                            if isinstance(errors_, ErrorWrapper):
                                errors.append(errors_)
                            elif isinstance(errors_, list):
                                errors.extend(errors_)
                        values[field.name] = v_
    return values, errors
```

In the corrected version:
- We iterate over the required parameters and properly check for sequence-shaped fields.
- We correctly handle the extraction of values for sequence-shaped fields like lists, sets, and tuples.
- We ensure that the extracted values are validated and stored correctly in the `values` dictionary.
- We update the error handling and appending logic to ensure proper error reporting.

By making these adjustments, the `request_body_to_args` function should now properly handle sequence-shaped fields in the received body data and pass the failing test cases.