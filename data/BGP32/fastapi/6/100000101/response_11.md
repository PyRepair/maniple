## Bug Explanation
The bug in the provided function `request_body_to_args` lies in the `embed` check where it sets the `received_body` to a dictionary with only one key when there is only one required parameter and that parameter does not have the embed attribute set to `True`. This behavior is incorrect as it overwrites the `received_body` variable, causing issues with processing the other required parameters.

## Bug Fix Strategy
To fix the bug, we need to remove the conditional assignment of `received_body` to a dictionary inside the loop. Instead, we should process each field independently based on whether it is a sequence or not.

## The Corrected Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []

    for field in required_params:
        value: Any = None
        field_info = get_field_info(field)

        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)

        if (
            value is None
            or (
                isinstance(field_info, params.Form)
                and field.shape in sequence_shapes
                and len(value) == 0
            )
        ):
            if field.required:
                if PYDANTIC_1:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig)
                    )
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if field.shape in sequence_shapes:
                awaitables = [sub_value.read() for sub_value in value]
                contents = await asyncio.gather(*awaitables)
                value = sequence_shape_to_type[field.shape](contents)
            elif isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
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

With this correction, the function should now correctly process the required parameters, handle sequences appropriately, and not overwrite the `received_body` variable unnecessarily.