### Bug Explanation
The bug in the `request_body_to_args` function arises from the incorrect handling of sequence values in the `received_body`. When multiple values are present in a sequence type (like a list, set, or tuple) in the `received_body`, the function does not process them correctly to extract all the values into a list, set, or tuple as required by the `required_params`.

### Bug Location
The primary issue lies in the handling of sequence shapes within the `received_body` processing logic. The function fails to correctly extract and assign sequence values to the corresponding field in the `required_params`.

### Fix Strategy
To fix the bug, we need to modify the logic responsible for processing sequence values in the `received_body`. Specifically, we should ensure that the function correctly extracts and assigns sequence values to the respective field in the `required_params`, accommodating lists, sets, and tuples accordingly.

### Corrected Function
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
                if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                    if isinstance(value, UploadFile):
                        value = await value.read()
                    elif isinstance(value, sequence_types):
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

The corrected version of the function should now correctly handle sequence values within the `received_body`, extracting and assigning them based on the respective `required_params`. This modification ensures that the function processes sequence shapes appropriately, generating the expected outputs for different sequence types.