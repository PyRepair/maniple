### Bug Explanation
The buggy function `request_body_to_args` is designed to process the required parameters and the received body to extract values and handle errors. The issue arises when handling fields that are lists, sets, or tuples due to incorrect processing of their elements within the FormData. The function fails to correctly handle these cases, resulting in erroneous values and errors being generated.

### Bug Identification
1. The function does not properly handle multiple values for a single alias when the field is a list, set, or tuple. It leads to incorrect categorization and processing of these values, causing the error wrappers to be appended inaccurately.
2. Errors such as ListError, SetError, and TupleError are added to the error list incorrectly without a valid basis, resulting in failure cases for specific shapes of fields.

### Bug Fix Strategy
To fix the bug, the function needs to properly parse the received body for list, set, and tuple fields. It should appropriately handle multiple values for the same alias and correctly categorize them based on the field shape. Additionally, error handling should be revised to ensure that errors are added only when necessary, based on the field types and received data.

### Corrected Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        alias = field.alias
        value = None

        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.shape == 1:
                    value = received_body.getlist(alias)
                elif field.shape == 2:
                    value = received_body.getlist(alias)
                else:
                    value = [(key, value) for key, value in received_body.multi_items() if key == alias]

            else:
                value = received_body.get(alias)

        if value is None or (isinstance(field_info, params.Form) and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", alias))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if field.shape == 1:
                value = value[0] if isinstance(value, list) and value else value
            v_, errors_ = field.validate(value, values, loc=("body", alias))

            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_

    return values, errors
```

This corrected version of the function addresses the issues related to processing list-based fields in FormData, ensures proper categorization of values based on the field shape, and accurately handles errors based on the field types.