### Bug Explanation
The buggy function `request_body_to_args` is designed to extract values from a dictionary or `FormData` object based on a list of required parameters and handle various cases, including sequence shapes and file uploads. The bug arises from how the function handles non-typing sequences like lists, sets, and tuples when passed as form data.

In the failing tests, the function fails to correctly process non-typing sequences when provided as form data, leading to errors related to the handling of these sequences. Specifically, the function does not properly handle non-typing sequences represented as lists, sets, or tuples in the form data, resulting in errors when trying to extract values for validation.

### Bug Fix Strategy
To fix the bug, the function should be updated to correctly handle non-typing sequences passed as form data. The correction involves identifying the type of sequence being used (list, set, tuple) and appropriately extracting and handling the values to avoid errors during validation. Additionally, the function should ensure that the extracted values match the expected type for the field being validated.

### Corrected Version of the Function
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
                # Extract values as list for non-typing sequences
                if field.shape == 0:  # list
                    value = received_body.getlist(field.alias)
                elif field.shape == 1:  # set
                    value = set(received_body.getlist(field.alias))
                elif field.shape == 2:  # tuple
                    value = tuple(received_body.getlist(field.alias))
            else:
                value = received_body.get(field.alias)
        if value is None or (isinstance(field_info, params.Form) and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
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
            values[field.name] = v_
    return values, errors
```

By updating the function to correctly handle non-typing sequences and extracting values based on the sequence shape, the corrected version should be able to pass the failing tests where non-typing sequences are provided as form data.