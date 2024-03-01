## Bug Explanation:
The bug in the `request_body_to_args` function arises from how the function handles data for fields with different shapes (list, set, tuple) and the corresponding values received in the `received_body` parameter. The function fails to correctly process data for non-typing sequences like lists, sets, and tuples causing the tests to fail. Additionally, the error handling logic for missing values is not correctly implemented, resulting in errors even when the values are present.

## Bug Fix Strategy:
1. Modify the function logic to correctly process non-typing sequences (lists, sets, tuples) from the `received_body`.
2. Update the error handling logic to only report errors for missing required fields.

## Corrected Version of the Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        field_info = get_field_info(field)
        value = None
        if received_body is not None:
            value = received_body.get(field.alias)
        
        if value is None or value == "":
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

With this corrected version of the function, the bug handling non-typing sequences and error reporting for missing values should be resolved. This updated function should now pass the failing tests.