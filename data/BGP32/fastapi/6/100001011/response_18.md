### Bug Explanation
The bug in the `request_body_to_args` function is related to handling multiple values for the same key in the `FormData` input. The function currently only captures the last value for a repeated key, leading to incorrect behavior and validation issues when dealing with repeated keys in form data.

### Bug Cause
1. The function currently overrides the received body dict with the last key-value pair when encountering a repeated key in the FormData input.
2. This behavior causes incorrect values to be assigned to the required parameters.
3. Consequently, this results in validation errors during field validation due to missing or incorrect values for the required parameters.

### Bug Fix Strategy
To fix this bug, we need to modify how the function handles repeated keys in the FormData input. Instead of overriding the received body dict, we should collect all values for a repeated key and assign them as a list before validation. This ensures that all values for a repeated key are available for validation and processing.

### Bug Fix
Here is the corrected version of the `request_body_to_args` function:

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
                    # Check if the field alias is present in the form data keys
                    if field.alias in received_body.keys():
                        # If the field alias exists, retrieve all values for that key
                        # as a list to handle repeated keys
                        value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            
            if (
                value is None
                or (isinstance(field_info, params.Form) and value == "")
                or (
                    isinstance(field_info, params.Form)
                    and field.shape in sequence_shapes
                    and len(value) == 0
                )
            ):
                if field.required:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            
            if (
                isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif (
                field.shape in sequence_shapes
                and isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, sequence_types)
            ):
                awaitables = [sub_value.read() for sub_value in value]
                contents = await asyncio.gather(*awaitables)
                value = sequence_shape_to_type[field.shape](contents)
                
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    
    return values, errors
```

In this corrected version, the function now correctly handles repeated keys in the FormData input by retrieving all values for a key as a list, allowing for proper validation and processing of input data.