The bug in the `request_body_to_args` function lies in how it handles non-typing sequence types like `list`, `set`, and `tuple`. The function fails to correctly extract and validate the values for these types from the received body, resulting in errors being appended when processing these types.

To fix the bug, we need to update the function to handle non-typing sequences properly. We can modify the function to check for non-typing sequence types and handle them accordingly.

Here is the corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    def extract_values(field: ModelField, value: Any) -> Any:
        if field.shape == 1:
            if isinstance(value, FormData):
                return value.getlist(field.alias)
            else:
                return value.get(field.alias)
        elif field.shape in sequence_shapes:
            if isinstance(value, FormData):
                return value.getlist(field.alias)
            else:
                return value
    
    for field in required_params:
        value = None
        if received_body is not None:
            value = extract_values(field, received_body)
        if value is None or (isinstance(field_info, params.Form) and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                if isinstance(value, UploadFile):
                    value = await value.read()
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, (ErrorWrapper, list)):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    
    return values, errors
```

This corrected version of the function should now handle non-typing sequence types like `list`, `set`, and `tuple` correctly, allowing the failing tests to pass with the expected input/output values.