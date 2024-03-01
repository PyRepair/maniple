### Bug Analysis:
1. The bug stems from the assumption that the received form data is in the correct format without considering the structure of non-typing sequences such as lists, sets, and tuples when parsing.
2. The function does not handle non-typing sequence shapes correctly, leading to errors in retrieving and processing the data.
3. The function incorrectly interprets the received form data as a single value instead of the actual sequence of values. This causes validation and processing issues, leading to incorrect error reporting and returned values.
4. To fix the bug, we need to adjust the logic for handling non-typing sequences in the form data and ensure that the values are correctly processed and validated according to the specified model fields.

### Bug Fix:
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
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    raw_values = received_body.getlist(field.alias)
                    if field.shape in (2, 3):
                        value = tuple(raw_values) if field.shape == 2 else set(raw_values)
                    else:  # shape == 1
                        value = raw_values
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
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```
In the fixed version of the function, we iterate through each required parameter field and handle different sequence shapes appropriately to extract the values from the form data. We create lists, sets, or tuples based on the specified shape of the field. This revision ensures that non-typing sequence structures are processed correctly by the function.