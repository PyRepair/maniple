### Bug Explanation:
The buggy function `request_body_to_args` is specifically designed to convert data from received bodies into arguments based on the required parameters provided. However, there are multiple issues in the function that are leading to failing tests. The function is not correctly handling sequence shapes like lists, sets, and tuples when they are provided in the `received_body`.

1. For the failed test related to a Python list parameter as a form, the function is not handling the list correctly when it is passed in the `received_body`. It is trying to access values based on the `field.alias` which is resulting in extracting only the last value from the list instead of the entire list.

2. Similarly, for the test with a Python set parameter as a form, the function is not handling the set correctly from the `received_body`, resulting in the same issue as the list.

3. Lastly, for the test with a Python tuple parameter as a form, the function is also not interpreting the tuple correctly, leading to extraction issues.

### Fix Strategy:
To fix the bug, the function needs to be updated to correctly handle sequence shapes like lists, sets, and tuples. The function should be modified to extract and parse these sequences as a whole, rather than extracting individual elements based on aliases.

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
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)

        if value is None or (isinstance(field_info, params.Form) and not value):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                value = await value.read()
            elif field.shape in sequence_shapes and isinstance(value, sequence_types):
                awaitables = [sub_value.read() for sub_value in value]
                contents = await asyncio.gather(*awaitables)
                value = sequence_shape_to_type[field.shape](contents)

            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_

    return values, errors
```

This corrected version should now handle sequences correctly and pass the failing tests.