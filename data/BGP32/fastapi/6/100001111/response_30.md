### Bug Explanation
The bug in the `request_body_to_args` function stems from the incorrect handling of repeated keys with multiple values in form data. The current implementation only considers the last value of a repeated key, leading to validation issues with expected lists, sets, or tuples. This behavior contradicts the expected behavior where multiple values per key should be treated as a collection (list, set, tuple) during validation.

The bug becomes evident in the failing tests where the function fails to correctly handle form data with multiple values for the same key and instead only takes the last value, causing validation errors.

### Bug Fix Strategy
To address the bug and align the function with the desired behavior stated in the GitHub issue, the function needs to be modified to handle repeated keys and their values properly. Specifically, when processing form data, the function should aggregate all values of a repeated key into a collection (list, set, tuple) rather than only considering the last value for validation.

### Corrected Version of the Function
Here is the corrected version of the `request_body_to_args` function:

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
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.alias in received_body:
                    value = received_body.getlist(field.alias)
                else:
                    value = []
            else:
                value = received_body.get(field.alias)

        if value is None:
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if isinstance(value, list) and lenient_issubclass(field.type_, list):
                v_ = value
            elif isinstance(value, set) and lenient_issubclass(field.type_, set):
                v_ = value
            elif isinstance(value, tuple) and lenient_issubclass(field.type_, tuple):
                v_ = value
            else:
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
            values[field.name] = v_

    return values, errors
```

In this corrected version, the function now correctly handles repeated keys in form data and aggregates their values into collections before validation. This change ensures that the behavior aligns with the expectations outlined in the GitHub issue.