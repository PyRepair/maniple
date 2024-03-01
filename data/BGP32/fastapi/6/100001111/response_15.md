The issue reported on GitHub indicates that when using FastAPI to handle repeated key=value pairs in form data, only the last key=value is considered, leading to issues with validation. The desired behavior is to collect all repeated keys and assign their values as a list before validation.

The buggy function `request_body_to_args` is responsible for processing required parameters and received body data, but it encounters issues with processing repeated keys in form data.

### Bug in the Buggy Function:
The bug arises when handling form data with repeated keys. The function only assigns the last value of the repeated key to the corresponding field, which leads to validation errors since the expected behavior should be to collect all values of the repeated key as a list.

### Fixing Strategy:
To address the bug, we need to modify the logic of the function to correctly handle repeated keys in form data. By collecting all values of the repeated key into a list and assigning it to the field, we can ensure that validation works as expected.

### Corrected Version of the Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value = []
        if received_body is not None:
            if field.alias in received_body:
                if isinstance(received_body[field.alias], list):
                    value = received_body.getlist(field.alias)
                else:
                    value.append(received_body.get(field.alias))
        if len(value) == 0 and field.required:
            errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
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

By revising the logic to collect all values of the repeated key using `getlist` if it is a list or appending single values to the list, we ensure that the function behaves correctly for form data with repeated keys. This correction aligns with the expected behavior described in the GitHub issue.