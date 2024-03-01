### Bug Explanation
The bug in the `request_body_to_args` function arises from the incorrect handling of sequence types (`list`, `set`, `tuple`) when parsing the received body data. The function fails to correctly extract values from the FormData based on the field aliases, leading to validation errors and status code 422 instead of the expected 200.

The bug manifests because the function incorrectly assumes that the received data corresponds directly to the field alias in the required parameters, leading to errors in value extraction and validation.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function correctly handles sequence types like lists, sets, and tuples when extracting values from the FormData. Specifically, we should extract and validate the values based on the correct field alias for each sequence type instead of assuming a direct correspondence.

### Corrected Function
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
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.alias in received_body:
                    value = received_body[field.alias]
                    if field.shape in sequence_shapes and not isinstance(value, list):
                        value = [value]
            else:
                value = received_body.get(field.alias)
        
        if value is None or value == "":
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if field.shape in sequence_shapes:
                value_list = value if isinstance(value, list) else [value]
                new_values = []
                for sub_value in value_list:
                    if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(sub_value, UploadFile):
                        sub_value = await sub_value.read()
                    new_values.append(sub_value)
                values[field.name] = sequence_shape_to_type[field.shape](new_values)
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

In the corrected function, we retrieve values from the FormData based on the correct field aliases for each required parameter, handle sequence types appropriately, and validate the values accordingly. This should address the extraction and validation issues observed in the failing tests.