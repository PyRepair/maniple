### Bug Explanation:
The bug in the `request_body_to_args` function arises from incorrect handling of sequences like lists, sets, and tuples in the `received_body`. The current implementation does not correctly parse these sequences from `FormData`. This results in the function not extracting the values correctly and failing to validate them, leading to the incorrect results seen in the failing tests.

### Bug Fixing Strategy:
To fix the bug, we need to update the function to properly handle all types of sequences in the `received_body`. This involves iterating over the field's values correctly, extracting them from `received_body`, validating them, and populating the `values` dictionary appropriately.

### Updated Corrected Function:
Here is the corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if received_body is not None:
        for field in required_params:
            value = None
            
            if isinstance(received_body, FormData):
                if field.alias in received_body:
                    value = received_body.getlist(field.alias) if field.shape in sequence_shapes else received_body.get(field.alias)
            
            if value is None or (
                isinstance(get_field_info(field), params.Form) and value == ""
            ) or (
                isinstance(get_field_info(field), params.Form)
                and field.shape in sequence_shapes
                and len(value) == 0
            ):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if field.shape in sequence_shapes:
                    value_list = [await sub_value.read() for sub_value in value]
                    value = sequence_shape_to_type[field.shape](value_list)
                elif isinstance(get_field_info(field), params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
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

Updating the function in this way should now correctly parse and extract sequences from `FormData`, validate them according to field requirements, and return the expected values and types. It should now pass all the failing tests provided.