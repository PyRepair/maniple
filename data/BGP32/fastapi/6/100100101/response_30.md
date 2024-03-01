### Bug Explanation
The buggy function `request_body_to_args` has a logic error in how it handles non-typing sequence shapes (list, set, tuple) for the field values. The function fails to correctly extract values from the FormData and convert them to the appropriate list, set, or tuple data types based on the field definitions.

### Bug Fix Strategy
To fix the bug, we need to update the logic in the function to correctly handle the extraction and conversion of values for non-typing sequence shapes. Specifically, we need to ensure that the received values are properly processed and converted to the expected data type (list, set, tuple) according to the field definitions.

### Updated Function

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value = None
        if received_body is not None:
            value = received_body.get(field.alias)
            if field.shape in sequence_shapes and isinstance(value, list):
                value = value
            elif field.shape in sequence_shapes and isinstance(value, str):
                value = [value]
            elif field.shape in sequence_shapes and isinstance(value, set):
                value = value
            elif field.shape in sequence_shapes and isinstance(value, tuple):
                value = list(value)
        
        if value is None and field.required:
            if PYDANTIC_1:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))

        if value is not None:
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            values[field.name] = v_ if errors_ is None else deepcopy(field.default)

    return values, errors
```

By updating the function with the corrected logic above, it should now correctly handle non-typing sequence shapes for field values and pass all the given test cases.