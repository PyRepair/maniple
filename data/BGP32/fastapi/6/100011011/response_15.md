### Analysis:
- The function `request_body_to_args` is responsible for extracting values from the received body based on required parameters.
- The error messages indicate that the function is not handling non-typing sequences (like list, set, tuple) correctly.
- Errors reported for each case suggest issues with the handling of sequence types in received data.
- The problematic behavior stems from incorrect handling of sequential data where the same key is provided multiple times in the FormData.
- The GitHub issue also highlights the problem with repeated key=value pairs in Form data and the need for proper handling.

### Bug Cause:
- The current implementation does not account for cases where the same key appears multiple times in `FormData`.
- The function incorrectly processes the received data and only considers the last value for a key, leading to validation errors.
- In the failing tests, the errors occur due to issues with handling multiple values for the same key in `FormData`.

### Bug Fix Strategy:
- In order to address the bug, the function needs to properly handle sequential data, especially when the same key is present multiple times in `FormData`.
- The fix should involve collecting all values for a key in `FormData` and treating them as a list when encountered, rather than discarding all but the last occurrence.
- An approach to resolve the bug is to modify the logic that extracts values from `FormData` and appropriately handles sequence types.

### Bug-fixed Version:
```python
from fastapi.datastructures import FormData
from pydantic.fields import Field as ModelField

async def request_body_to_args(
    required_params: List[ModelField], received_body: Optional[Union[Dict[str, Any], FormData]]
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:        
        for field in required_params:
            value = received_body.getlist(field.alias) if isinstance(received_body, FormData) else received_body.get(field.alias)
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

### Updated Function Explanation:
- The revised implementation correctly checks for data in `FormData` and retrieves all values for a key as a list using `getlist`.
- It ensures that all values related to a key in `FormData` are considered for validation, preventing the issue of discarding multiple occurrences of the same key.
- This fix aligns with the expected behavior where all values for a key are accounted for, addressing the bug reported in the failing tests and GitHub issue.