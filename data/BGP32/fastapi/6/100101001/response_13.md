### Bug Explanation:
The bug in the `request_body_to_args` function stems from the incorrect handling of non-typing sequences (`list`, `set`, `tuple`) in the `received_body`. The function processes the fields considering only `FormData` values, which leads to errors when dealing with non-typing sequences. This results in the failing tests due to the incorrect interpretation of the received data.

### Bug Fix Strategy:
To fix the bug, the function needs to provide proper handling for non-typing sequences in the `received_body`. Specifically, it should ensure that when processing fields of type `list`, `set`, or `tuple`, the values are correctly extracted and handled from the `received_body` even if it is of type `FormData`.

### Corrected Version of the Function:
Below is the corrected version of the `request_body_to_args` function:

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
                if field.shape in sequence_shapes:
                    value = received_body.getlist(field.alias) if isinstance(received_body, FormData) else received_body.get(field.alias)
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

### Outcome:
After implementing the fix and using the corrected version of the `request_body_to_args` function, the failing tests related to handling non-typing sequences like `list`, `set`, and `tuple` should pass successfully. Make sure to test the corrected function thoroughly with different scenarios to verify its correctness.