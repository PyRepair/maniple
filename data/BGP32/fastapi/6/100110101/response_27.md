## Analysis
1. The `request_body_to_args` function is responsible for processing required parameters and received body data and preparing them for validation.
2. The function loops through the required parameters and retrieves values from the received body based on the parameter aliases.
3. Errors can occur if the field is required but missing in the received body or if there are validation errors while processing the values.
4. The function handles different types of fields, including those that need file reading.
5. The failing tests indicate an issue with the function when dealing with sequence-shaped fields and processing received body data correctly.

## Identified Issue
The issue arises when handling parameters with sequence shapes (list, set, tuple) from FormData. The current logic does not correctly process these sequences, leading to validation errors and incorrect return values.

## Bug Fix Strategy
To fix the bug, we need to update the logic to correctly handle sequence-shaped fields and extract data from FormData appropriately. This involves checking the type of field and dealing with sequence shapes distinctively.

## Bug-fixed Version
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
            if field.shape in sequence_shapes and isinstance(value, sequence_types):
                value = value if field.shape == 2 else tuple(value)
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

In this corrected version, we have modified the logic to correctly handle sequence-shaped fields (`list`, `set`, `tuple`) from `FormData` while processing the received data. This fix should resolve the issues identified in the failing tests while also satisfying the expected input/output values in various scenarios.