### Bug Explanation:
The bug in the `request_body_to_args` function occurs when handling non-typing sequences (list, set, tuple) as form data. The function incorrectly processes these sequences, resulting in validation errors and incorrect values being returned. The bug arises from not properly handling non-typing sequences such as sets and tuples when received as form data.

### Bug Fix Strategy:
To fix the bug, we need to update the function to correctly handle non-typing sequences like lists, sets, and tuples when received as form data. The function should properly validate and process these sequence types to ensure that the values are correctly extracted and errors are handled.

### Corrected Function:
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
            if field.shape == 1 and isinstance(received_body, FormData):
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)

            if value is None or value == "":
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
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

The corrected function now properly handles non-typing sequences like lists, sets, and tuples when received as form data, ensuring correct validation and value extraction. This updated version should now pass the failing tests provided.