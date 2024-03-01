### Bug Explanation:
The buggy function `request_body_to_args` is designed to extract values from the `received_body` parameter corresponding to the required parameters defined in `required_params`. It checks if the `received_body` contains the required fields and constructs a dictionary of values while also collecting any errors encountered during the validation process.

However, the bug in the function is related to the processing of non-typing sequence shapes (list, set, tuple) such as they are not handled correctly when processing as form data using `FormData`. The function fails to correctly extract the values for non-typing sequence types causing validation errors resulting in status code 422 instead of the expected 200.

The issue arises when trying to retrieve the values for non-typing sequences directly from the `received_body`. The provided implementation does not handle this scenario adequately, leading to validation issues.

### Bug Fix Strategy:
To fix the bug, the function needs to correctly handle non-typing sequence shapes (list, set, tuple) when processing them as form data using `FormData`. We need to modify the logic to extract these values correctly to ensure proper validation.

### Corrected Function:
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
            if isinstance(field.type_, list) and isinstance(received_body, FormData):
                value = received_body.getlist(field.alias)
            elif isinstance(field.type_, set) and isinstance(received_body, FormData):
                value = set(received_body.getlist(field.alias))
            else:
                value = received_body.get(field.alias)

            if value is None:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
                    continue

            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
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

By updating the function logic to correctly handle non-typing sequence types in the `received_body`, the function should now be able to extract the values for such cases and perform the validation appropriately. This corrected version should now pass the failing tests with a status code of 200 for the provided cases.