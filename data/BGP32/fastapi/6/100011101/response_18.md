### Bug Explanation
The bug in the `request_body_to_args` function arises from how it handles form data for non-typing sequences (list, set, tuple). The function does not correctly interpret these data structures when processing form data, resulting in validation errors even when the input data is valid. The bug is related to the processing of sequences and incorrectly handling the conversion of sequence elements.

### Bug Fix Strategy
To fix the bug, the function should correctly process form data for non-typing sequences by intelligently handling the conversion of elements into the appropriate data structure. Additionally, the function should handle the reading and validation of non-typing sequences like lists, sets, and tuples in form data.

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
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(
                received_body, FormData
            ):
                if field.alias in received_body:
                    value = received_body.getlist(field.alias)
                else:
                    value = None
            else:
                value = received_body.get(field.alias)
        if value is None:
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
        if isinstance(field_info, params.File):
            value = await value.read() if isinstance(value, UploadFile) else None
        elif field.shape in sequence_shapes and isinstance(value, sequence_types):
            awaitables = [sub_value.read() for sub_value in value]
            contents = await asyncio.gather(*awaitables)
            value = sequence_shape_to_type[field.shape](contents)
        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_
    return values, errors
```

With this corrected version of the `request_body_to_args` function, the handling of non-typing sequences in form data should now function correctly, allowing the function to process and validate them without causing validation errors.