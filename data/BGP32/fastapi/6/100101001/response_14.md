### Bug Explanation:
The bug in the `request_body_to_args` function lies in the way it handles non-typing sequences (list, set, tuple) in the received body. When processing non-typing sequences, the function fails to correctly extract the values from the FormData and validate them, leading to errors in the form of `ErrorWrapper` objects.

In the provided test cases, the function fails to handle non-typing sequences like lists, sets, and tuples correctly. As a result, it generates errors during validation and fails to return the expected values.

### Bug Fix Strategy:
To fix the bug, we need to update the logic in the `request_body_to_args` function to properly handle non-typing sequences in the received body. This involves correctly extracting values from the FormData, validating them, and populating the `values` dictionary accordingly.

### Corrected Version of the Function:
Here is the corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    sequence_types = list, set, tuple
    if required_params:
        field = required_params[0]
        field_info = get_field_info(field)
        embed = getattr(field_info, "embed", None)
        if len(required_params) == 1 and not embed:
            received_body = {field.alias: received_body}
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if isinstance(received_body, FormData):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            if value is None or isinstance(field_info, params.Form) and value == "":
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.alias] = deepcopy(field.default)
                continue
            if (
                isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.alias] = v_
    return values, errors
```

This corrected version addresses the issue with handling non-typing sequences correctly and should now pass the failing tests provided.