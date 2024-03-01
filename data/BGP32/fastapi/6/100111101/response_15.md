After analyzing the buggy function and the failing tests, it seems that the issue lies in how the function handles sequence-shaped fields in FormData for list, set, and tuple types. The current implementation fails to properly extract values from FormData when dealing with sequence-shaped fields.

To fix this bug, we need to modify the logic inside the `request_body_to_args` function to correctly handle sequence-shaped fields when extracting values from FormData.

Here is the corrected version of the function:

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
                    # For sequence-shaped fields, get all values with the alias
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            
            if value is None:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
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

With this corrected version, the function should now handle sequence-shaped fields correctly when extracting values from FormData. This fix should allow the failing tests to pass as the function now properly processes list, set, and tuple types within FormData.