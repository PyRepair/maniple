### Analysis
The buggy function `request_body_to_args` is responsible for converting request body parameters into arguments. The issue specified relates to supporting repeated key=value pairs in form data for validation purposes.

The buggy function logic does not handle the scenario where multiple values are associated with the same key in the `received_body`, resulting in only the last value being considered. This behavior contradicts the expected outcome when using `Form` as the parameter type for repeated keys.

### Bug Cause
The bug arises from the section of the code where the value associated with a field's alias is retrieved from the `received_body`. When the same key appears multiple times in the `FormData`, only the last value is extracted, leading to incorrect processing and validation of data.

### Bug Fix Strategy
To resolve the bug and support repeated key=value pairs in the `FormData`, the function needs to be modified to properly handle this scenario. All values associated with the same key should be collected and treated as a list before validation occurs.

### Bug-fixed Version
Below is the corrected version of the `request_body_to_args` function that addresses the bug:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = {}
    if required_params:
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    values[field.name] = received_body.getlist(field.alias)
                else:
                    raw_values = received_body.get(field.alias)
                    if raw_values is not None:
                        if isinstance(raw_values, list):
                            values[field.name] = raw_values
                        else:
                            values[field.name] = [raw_values]
            if field.required and values.get(field.name) is None:
                errors[field.name] = [ErrorWrapper(MissingError(), loc=("body", field.alias))]
    return values, list(errors.values())
```

### Explanation of Changes
- Modified the processing of the `received_body` to correctly handle repeated keys by collecting all associated values as a list.
- Adjusted the error collection logic to store errors based on the field names for better error reporting consistency.

By applying these changes, the function now supports repeated key=value pairs in the `FormData`, aligning with the expected behavior described in the GitHub issue.