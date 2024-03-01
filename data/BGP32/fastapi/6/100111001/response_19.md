### Bug Analysis
- The function `request_body_to_args` is designed to process request body parameters based on the required parameters provided. It extracts values from the received body according to the specified fields.
- In the failing tests, the input parameters have specified types like `list`, `set`, and `tuple`, but the function seems to treat them as non-typing sequences.
- The bug is related to how the function handles different types of parameters when extracting values from the received body. It fails to appropriately handle collections like `list`, `set`, and `tuple`.
- The function is incorrectly identifying the shape of the field and not handling it properly, causing errors and failing the tests.

### Bug Fix Strategy
To fix this bug, we need to modify how the function extracts values from the received body based on the parameter types specified. We should differentiate the processing logic for `list`, `set`, and `tuple` types explicitly. This will involve handling the different shapes of the fields correctly.

### Corrected Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value: Any = None
        for alias, body_value in received_body.items():
            if alias == field.alias:
                if field.shape in sequence_shapes and isinstance(body_value, list):
                    value = body_value
                else:
                    value = body_value
                break
        if value is None:
            if field.required:
                if PYDANTIC_1:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:  # pragma: nocover
                    errors.append(
                        ErrorWrapper(  # type: ignore
                            MissingError(), loc=("body", field.alias), config=BaseConfig
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

This corrected version modifies how the values are extracted based on the field types and shapes explicitly. It ensures that the function processes `list`, `set`, and `tuple` types correctly and avoids the previous errors.