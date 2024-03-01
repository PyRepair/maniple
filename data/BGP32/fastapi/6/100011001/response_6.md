### Bug Explanation
The bug in the `request_body_to_args` function occurs due to the incorrect handling of sequence-shaped fields when they are received in the request body. The function fails to properly extract and validate the values for fields that are sequential (like lists, sets, tuples) when they are received as form data. This results in validation errors and a status code of 422 instead of 200 in the tests.

The function incorrectly processes the value for `field.shape` and does not handle sequence-shaped fields correctly when received as `FormData`. It fails to extract the correct values from the form data for sequential fields, leading to validation errors.

### Bug Fix Strategy
To fix the bug, the function needs to be adjusted to correctly handle sequence-shaped fields (list, set, tuple) when they are received in the form data. This involves properly extracting the values corresponding to these fields and validating them accordingly.

### Corrected Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    sequence_shapes = {list, set, tuple}
    if required_params:
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            if value is None:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if isinstance(value, list) and field.type_ == list:
                    v_ = value
                elif isinstance(value, set) and field.type_ == set:
                    v_ = set(value)
                elif isinstance(value, tuple) and field.type_ == tuple:
                    v_ = tuple(value)
                else:
                    v_ = value
                
                v_, errors_ = field.validate(v_, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
            
    return values, errors
```

This corrected version of the function now properly handles sequence-shaped fields when received in the form data, ensuring that the values are extracted, validated, and stored correctly. This fix should address the bug and allow the tests to pass with a status code of 200.