## Bug Explanation:
The bug in the `request_body_to_args` function arises from the incorrect handling of non-typing sequences like lists, sets, and tuples when converting them from FormData. The function fails to properly extract the values from the FormData and assign them to the correct fields, leading to validation errors and incorrect output.

## Bug Identification:
- The function does not handle non-typing sequences appropriately, leading to errors when extracting values.
- There are issues related to the validation of the received data that prevent the correct values from being stored in the `values` dictionary.

## Bug Fix Strategy:
1. Ensure that the function correctly handles non-typing sequences such as lists, sets, and tuples extracted from FormData.
2. Verify that the values are properly extracted from the FormData and assigned to the correct fields.
3. Fix the validation logic to prevent unnecessary errors and ensure that the correct values are stored in the `values` dictionary.

## Corrected Version of the Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
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
            or (isinstance(get_field_info(field), params.Form) and not value)
        ):
            if field.required:
                if PYDANTIC_1:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:  # pragma: nocover
                    errors.append(
                        ErrorWrapper(
                            MissingError(), loc=("body", field.alias), config=BaseConfig
                        )
                    )
            else:
                values[field.name] = deepcopy(field.default)
            continue
        if (
            isinstance(get_field_info(field), params.File)
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

By implementing the above corrections in the `request_body_to_args` function, it should now handle non-typing sequences correctly when extracting values from FormData and storing them in the `values` dictionary. The updated function should pass the failing tests and produce the expected output.