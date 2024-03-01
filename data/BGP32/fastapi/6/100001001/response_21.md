## Bug Analysis
The bug in the `request_body_to_args` function is related to how the function processes a sequence of values in the body data when the parameter expects a sequence type (list, set, tuple, etc.). The function incorrectly handles the case when the received body data is a `FormData` object and the parameter shape is considered a sequence.

### Issues
1. The function does not correctly handle sequence shapes when processing the received body.
2. The logic to extract values from the body, especially for multiple values (e.g., a list), is faulty.

### Root Cause
The bug arises from incorrectly processing sequence-shaped fields in the `received_body` when the body data is of type `FormData`.

## Bug Fix Strategy
To fix the bug, we need to revisit how sequence-shaped fields are processed in the presence of FormData. We should ensure that each field in a sequence is extracted correctly and processed based on its shape.

### Updated Function
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
                    if field.alias in received_body:
                        value = received_body.getlist(field.alias)
                    else:
                        value = []
                else:
                    value = received_body.get(field.alias)
                    
            if value is None or (isinstance(field_info, params.Form) and value == ""):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
                continue
                
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                value = await value.read()
            elif field.shape in sequence_shapes and isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
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

This updated version fixes the handling of sequence-shaped fields in the presence of FormData and ensures correct extraction and processing of values.