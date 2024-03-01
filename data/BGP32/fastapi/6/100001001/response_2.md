## Bug Explanation
The bug in the provided function `request_body_to_args` arises from how the function is handling fields of different types (list, set, tuple) within the `required_params` list. The function incorrectly assumes the type of the field based on the `shape` attribute, which leads to incorrect type validation and error reporting.

### Issues:
1. The function treats all fields as having a `shape` attribute and checks them against `sequence_shapes`, leading to incorrect processing and validation for non-list fields.
2. Incorrect error types (ListError, SetError, TupleError) are used when generating errors, which may not align with the actual type validation issue.

## Bug Fix Strategy
To fix the bug, we need to:
1. Remove the reliance on the `shape` attribute to determine type validation logic.
2. Update the error handling to use more generic error types for better consistency.

## Bug-free Function
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
            if isinstance(received_body, FormData):
                value = received_body.get(field.alias)

        if value is None or (isinstance(field, params.Form) and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
            continue

        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_

    return values, errors
```

With this correction, the function should properly handle different field types and generate error wrappers consistently for invalid values.