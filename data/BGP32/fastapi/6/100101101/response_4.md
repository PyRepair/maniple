## Bug Explanation
The buggy function `request_body_to_args` fails to handle input data when the required parameter is of type `list`, `set`, or `tuple` and the received data is in the form of `FormData`. It incorrectly processes the values and generates errors, leading to failing test cases.

### Issues:
1. For the `list` case, the function wrongly converts the received data to a single value instead of a list of values.
2. For the `set` case, the function produces an error rather than correctly handling the set conversion.
3. For the `tuple` case, the function doesn't extract the received values into a tuple correctly.

## Bug Fix Strategy
To fix the bug, the function needs to properly handle the cases of converting `list`, `set`, and `tuple` from FormData. The fix should involve identifying the appropriate conversion for each data type and ensuring that the received values are processed correctly for each case.

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
        if received_body is not None:
            if isinstance(received_body, FormData):
                if field.shape in sequence_shapes:
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
        if value is None or (
            isinstance(field_info, params.Form)
            and field.shape in sequence_shapes
            and len(value) == 0
        ):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                if field.shape not in sequence_shapes:
                    if isinstance(value, list):
                        value = [v.encode() if isinstance(v, str) else v for v in value]
                else:
                    awaitables = [sub_value.encode() if isinstance(sub_value, str) else sub_value.read() for sub_value in value]
                    value = sequence_shape_to_type[field.shape](await asyncio.gather(*awaitables))
            elif field.shape in sequence_shapes and isinstance(value, sequence_types):
                awaitables = [sub_value.encode() if isinstance(sub_value, str) else sub_value.read() for sub_value in value]
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

The corrected function should now properly convert the received data into lists or other appropriate data types based on the required parameter field type, resolving the issues leading to failing test cases.