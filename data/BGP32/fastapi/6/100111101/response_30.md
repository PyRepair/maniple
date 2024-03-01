The bug in the `request_body_to_args` function seems to be related to how the function handles different types of input data and shapes. Specifically, for non-primitive types like lists, sets, and tuples, the function fails to correctly process the data leading to validation errors.

The issue stems from the logic where the function tries to extract values from the `received_body` based on the input field's alias. For non-primitive types, the function incorrectly processes the data leading to incorrect validations and error wrappers being added to the `errors` list.

To fix this bug, we need to update the logic of how non-primitive types are handled, ensuring that the function correctly extracts and processes the data before validation.

Here is a corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        field_info = get_field_info(field)
        value = None
        if received_body is not None:
            if isinstance(received_body, FormData):
                if field.shape in sequence_shapes:
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
        if value is None or (isinstance(field_info, params.Form) and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if (
                field.shape in sequence_shapes
                and isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
            ):
                if isinstance(value, (list, set)):
                    value = list(value)
                elif not isinstance(value, list):
                    value = [value]
                value = [await v.read() if isinstance(v, UploadFile) else v for v in value]
                if field.shape == 2:
                    value = tuple(value)
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

This corrected version of the function should now correctly handle different types of input data and shapes for non-primitive types like lists, sets, and tuples. It ensures that the data is processed correctly before validation, preventing validation errors and providing the expected output values for the failing tests.