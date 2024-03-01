The main issue in the `request_body_to_args` function is with how it handles multiple values associated with the same key in the `FormData`. Also, the logic for validating and processing array-like shapes (list, set, tuple) needs to be improved to correctly create the desired response.

### Bug Explanation:
1. In the provided test cases, when handling a sequence shape parameter (list, set, tuple) with data coming in as FormData, the function fails to properly extract and process multiple values for the same key, resulting in validation errors.
2. Due to this issue, the function fails to correctly handle input data for list, set, and tuple types and generates validation errors based on erroneous assumptions about the received data format.
3. The errors arise from a mismatch between the expected behavior of the function (correctly parsing and validating sequence-shaped data) and the actual processing logic which does not account for multi-valued keys in FormData.

### Suggested Fix Strategy:
1. Revise the logic for handling sequence shape data (list, set, tuple) to correctly extract and process multiple values for the same key when receiving FormData input.
2. Update the function to handle different sequence shapes based on the parameter type and appropriately validate and construct responses for list, set, and tuple shapes.

### Corrected Version of the Function:
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
                    if field.alias in received_body:
                        value = received_body.getlist(field.alias)
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
                continue
            if (
                isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif field.shape in sequence_shapes:
                if field.type_ == list:
                    value = value
                elif field.type_ == set:
                    value = set(value)
                elif field.type_ == tuple:
                    value = tuple(value)
                
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.alias] = v_

    return values, errors
```

By making these changes, the corrected function should now properly handle validating and processing sequence-shaped data coming from FormData and correctly construct the desired output.