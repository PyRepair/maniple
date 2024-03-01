### Analysis and Explanation:
1. The function `request_body_to_args` is designed to convert received body data into arguments based on required parameters. It iterates through the required parameters list and validates the data against the received body.
   
2. The failing tests indicate that the status code returned is `422` which implies a validation error, while the expected status code is `200`. This discrepancy suggests that the function is not correctly handling the data validation for non-typing sequences like list, set, and tuple.

3. The error likely stems from how the function is handling parsing and validating the received body and assigning the values to the arguments. It seems that the current implementation is not properly handling the conversion for non-typing sequences.

4. To fix this bug, we need to modify the section of the function where it processes the data for non-typing sequences. We should ensure that the data is correctly validated and assigned to the arguments based on the sequence type (list, set, tuple).

### Bug Fix Strategy:
1. Update the code to properly handle the conversion and assignment of values for non-typing sequences like list, set, and tuple.
2. Ensure that the validations are correctly performed, and the values are assigned according to the type of sequence.
3. Make necessary adjustments to accommodate the correct data transformation for each type of sequence.

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
                    value = received_body.getlist(field.alias)
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
                and isinstance(value, list)
            ):
                values[field.name] = value
                continue

            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_

    return values, errors
```

This corrected version of the function should address the bug by ensuring that the data for non-typing sequences is appropriately validated and assigned to the arguments. This update should allow the function to correctly handle non-typing sequence types like list, set, and tuple, fixing the failing test cases.