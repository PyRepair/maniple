### Bug Analysis:
- The `request_body_to_args` function is responsible for converting received body data into arguments based on required parameters.
- The bug appears to stem from incorrectly handling sequence data types (list, set, tuple) in form data, resulting in errors when validating the values.
- The issue arises from treating each value of a repeated key in form data as a separate entity rather than aggregating them into a list for sequence types.

### Bug Cause:
- The bug occurs due to the handling of sequence shapes in the received form data. Each value of a repeated key is processed individually, leading to validation errors for sequence types.

### Proposed Fix Strategy:
- Modify the logic to aggregate repeated keys into a list for sequence types during data processing from form data.
- Ensure that the values for repeated keys are correctly consolidated before validation.

### Corrected Version of the Function:
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
                if isinstance(received_body, FormData):
                    if field.alias in received_body:
                        value = received_body.getlist(field.alias)
            if value is None:
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
In this corrected version, the function ensures that for sequence shapes (list, set, tuple), repeated keys in form data are collected into a list before validation. This modification addresses the root cause of the bug and aligns with the expected behavior outlined in the GitHub issue.