### Bug Explanation
The bug in the `request_body_to_args` function is related to how it handles parsing values from the received body when dealing with different types of sequences like lists, sets, and tuples. The function fails to correctly process incoming data, leading to validation errors and incorrect values in the output.

Specifically, the function incorrectly handles the case where the field shape is a sequence (like list, set, tuple) and the received body is a `FormData`. It attempts to retrieve values using `getlist` for a list shape, but this method does not work correctly for other sequence shapes (set, tuple). This results in incorrect or missing values for non-list shapes, causing the validation process to fail and errors to be generated.

### Bug Fix Strategy
To fix the bug, the function needs to handle different sequence shapes properly when extracting values from the received body. Depending on the shape of the field and the type of sequence, the function should retrieve the values correctly and process them accordingly. By addressing this issue, the function should be able to correctly parse and validate values from the received body for different sequence shapes.

### Corrected Function
Here is the corrected version of the `request_body_to_args` function:

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
                if field.shape == 1:  # Check if field shape is a sequence
                    if isinstance(received_body, FormData):
                        if field.type_ == list:
                            value = received_body.getlist(field.alias)
                        elif field.type_ == set:
                            value = set(received_body.getlist(field.alias))
                        elif field.type_ == tuple:
                            value = tuple(received_body.getlist(field.alias))
                else:
                    value = received_body.get(field.alias)
            if value is None or (isinstance(value, list) and len(value) == 0):
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

With this corrected version, the function should now be able to correctly extract and process values from the received body for various sequence shapes, ensuring that data is handled appropriately and validation errors are avoided.