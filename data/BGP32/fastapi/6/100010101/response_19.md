### Analysis:
- The buggy function is supposed to convert a request body to arguments based on the required parameters provided and the received body.
- The error message indicates that the function is returning a status code of 422 instead of the expected 200 for the tests involving non-typing sequences like lists, sets, and tuples.
- The bug likely stems from the way the function processes sequence-shaped fields in the request body.

### Issues:
1. The function does not correctly handle sequence-shaped fields (like lists, sets, and tuples) in the received body. It directly extracts the value without considering that these fields might contain multiple values.
2. There is an issue with handling sequence-shaped fields and conversion to the expected data type.

### Bug Fix Strategy:
1. Update the logic for processing sequence-shaped fields in the received body to extract all values appropriately to handle the scenario where multiple values are present in the field.
2. Ensure correct handling of different sequence shapes (e.g., lists, sets, tuples) when converting them to the expected data type.

### Corrected Function:
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
            if field.shape and isinstance(received_body, FormData):
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

### Explanation:
- The corrected function now properly handles sequence-shaped fields by extracting all values using `getlist()` when the field has a shape, and the received body is of type `FormData`.
- It correctly validates the extracted values and updates the values dictionary accordingly.
- This fix addresses the issues identified and ensures that the function processes non-typing sequences correctly, passing the failing tests.