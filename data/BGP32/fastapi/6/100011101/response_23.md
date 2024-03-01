### Bug Explanation
The bug in the `request_body_to_args` function arises from how it handles sequences like lists, sets, and tuples when passed in the `received_body` parameter. The function fails to correctly extract and validate the values for these sequences, leading to the incorrect creation of errors and wrong return values.

When sequences like lists, sets, or tuples are passed through `FormData`, the function incorrectly processes them, resulting in errors and failing validations. This behavior causes the function to return with status code `422` instead of `200`.

### Bug Fix Strategy
To fix the bug:
1. Correctly parse and extract the values for sequences from the `received_body` parameter.
2. Validate the values based on the specified parameters.
3. Ensure that errors are handled correctly to avoid returning incorrect status codes.

### Corrected Version of the Function
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
            if value is None or value == "":
                if field.required:
                    errors.append(
                        ErrorWrapper(
                            MissingError(),
                            loc=("body", field.alias)
                        )
                    )
            elif field.type_ in (list, set, tuple):
                if field.shape in sequence_shapes:
                    # Convert the values of the sequence to the correct type
                    value = field.shape(value)
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

By making the corrections above, the `request_body_to_args` function should now correctly handle sequences passed through `FormData` and validate them according to the specified parameters, resulting in the correct status code `200`.