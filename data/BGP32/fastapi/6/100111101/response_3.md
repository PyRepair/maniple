### Bug Explanation

The bug in the `request_body_to_args` function lies in how it handles non-typing sequences (`list`, `set`, `tuple`) when converting them from the received body to the expected values. The function attempts to read the values from the `FormData` object using the `get` and `getlist` methods, but it doesn't correctly handle form data with multiple values for the same key, resulting in only the last value being extracted.

### Bug Fix Strategy

To fix the bug, we need to modify the function to properly handle non-typing sequences when reading values from the `FormData` object. Specifically, when a field representing a non-typing sequence is encountered, we need to ensure that all values associated with that field alias are retrieved and passed to the validation step.

### Updated Corrected Version of the Function

Here is the corrected version of the `request_body_to_args` function that addresses the bug:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        alias = field.alias
        if isinstance(received_body, FormData):
            values[alias] = received_body.getlist(alias)
        else:
            values[alias] = received_body.get(alias) if received_body is not None else None

        field_info = get_field_info(field)
        if values[alias] is None or values[alias] == "":
            if field.required:
                if PYDANTIC_1:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", alias)))
                else:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", alias), config=BaseConfig))
            else:
                values.pop(alias, None)
                values[field.name] = deepcopy(field.default)
        elif isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
            if field.shape in sequence_shapes:
                awaitables = [uv.read() for uv in values[alias]]
                contents = await asyncio.gather(*awaitables)
                values[alias] = sequence_shape_to_type[field.shape](contents)
            else:
                values[alias] = await values[alias].read()
        else:
            if field.shape in sequence_shapes:
                values[alias] = sequence_shape_to_type[field.shape](values[alias])

        v_, errors_ = field.validate(values[alias], values, loc=("body", alias))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_

    return values, errors
```

The corrected version of the function now correctly processes non-typing sequences within the `FormData` object and populates the `values` dictionary accordingly. This fix should ensure that the function can handle non-typing sequences as form data and pass the failing tests successfully.