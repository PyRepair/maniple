The bug in the provided function `request_body_to_args` is related to handling repeated keys in form data. The function is designed to extract values from the received body (which can be a dictionary or FormData) based on the required parameters provided to it. However, the function does not correctly handle cases where the same key appears multiple times in FormData.

The bug arises because the function only captures the last value associated with the key in the FormData instead of collecting all values into a list when there are repeated keys.

To fix this issue and align the function with the requirements mentioned in the GitHub issue, we need to modify the logic to handle repeated keys properly and store multiple values associated with the same key in a list before further processing.

Here is the corrected version of the function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params and received_body:
        for field in required_params:
            value: Any = None
            if isinstance(received_body, FormData):
                if field.shape in sequence_shapes:
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            if value is None or (isinstance(field.info, params.Form) and value == ""):
                if field.required:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                values[field.name] = value
    return values, errors
```

With this correction, the function now correctly collects all values associated with the same key from the FormData and stores them as a list before validation. This modification addresses the issue reported on GitHub related to handling repeated key-value pairs in form data.

Please test the corrected function with the provided cases to ensure it meets the expected input/output requirements and fixes the bug.