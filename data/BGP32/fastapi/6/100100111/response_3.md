### Analysis:
1. The buggy function `request_body_to_args` is responsible for converting request body parameters to arguments for request processing. It processes each required parameter and maps them to the corresponding values in the received body data.
2. The function seems to have issues when handling sequence shapes and form data types.
3. The failing tests provided involve submitting various lists, sets, and tuples as form data and expecting them to be correctly processed and validated by the fast API. The function is currently unable to handle repeated keys properly.
4. To fix the bug, we need to enhance the logic for handling sequence shapes in the provided form data.

### Bug Cause:
The bug causes the function `request_body_to_args` not to process repeated keys in form data correctly. This discrepancy results in not being able to handle lists, sets, or tuples as expected. The code fails to properly map the received form data with multiple values to the required parameter type.

### Bug Fix Strategy:
To fix the bug, we need to update the logic in the function to handle repeated keys in the form data. By modifying the handling of `received_body` with repeated keys like `choices=parrot&choices=spider` to be collected as lists before validation, we can resolve the issue.

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
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    values[field.alias] = received_body.getlist(field.alias)
                else:
                    values[field.alias] = received_body.get(field.alias)
            if values[field.alias] is None:
                if field.required:
                    if PYDANTIC_1:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig)
                        )
                else:
                    values[field.name] = deepcopy(field.default)
                    continue
            
            v_, errors_ = field.validate(values[field.alias], values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

After applying this correction, the function `request_body_to_args` should handle repeated keys in the form data correctly, allowing the fast API to work with lists, sets, and tuples as form parameters as expected.