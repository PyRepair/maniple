### Bug identification and explanation:

The buggy function `request_body_to_args` is designed to extract values from a received body (either a dictionary or `FormData`) based on a list of required parameters (`required_params`). The bug in the function lies in how it handles non-typing sequences (lists, sets, tuples) within the received body. The function currently only extracts the last item from the non-typing sequence, leading to incorrect behavior and causing the failing tests.

#### Issue in the code:
- When dealing with non-typing sequences like lists, sets, and tuples in the received body, the function only considers the last item instead of extracting all items correctly.

### Bug fix strategy:

1. Update the logic responsible for how non-typing sequences are handled within the received body to correctly extract all items present in the sequence.
2. Modify the handling of non-typing sequences to account for lists, sets, and tuples separately.

### Corrected version of the function:
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
                    if field.type_ == list:
                        value = received_body.getlist(field.alias)
                    elif field.type_ == set:
                        value = set(received_body.getlist(field.alias))
                    elif field.type_ == tuple:
                        value = tuple(received_body.getlist(field.alias))
                    else:
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
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

By updating the logic to correctly handle non-typing sequences based on their type (list, set, tuple), the corrected version of the function should now be able to handle the failing tests appropriately and provide the expected results.