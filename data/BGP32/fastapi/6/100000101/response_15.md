The bug in the provided function is related to the handling of sequence values in the received body. When the received body contains multiple values for a field, the function fails to correctly extract and process these values based on the field's type.

To fix the bug, we need to ensure proper extraction of values for sequence-shaped fields (list, set, tuple) from the received body and handle them accordingly based on the field's type.

Here is the corrected version of the function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    sequence_shapes = {list, set, tuple}
    
    for field in required_params:
        field_info = get_field_info(field)
        embed = getattr(field_info, "embed", None)
        value: Any = None
        
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if embed:
                    value = [received_body.get(field.alias, [])]
                else:
                    value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
        
        if value is None or (
            isinstance(field_info, params.Form)
            and field.required
            and ((field.shape in sequence_shapes and len(value) == 0) or value == "")
        ):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                value = await value.read()
            elif field.shape in sequence_shapes and isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
                awaitables = [sub_value.read() for sub_value in value]
                contents = await asyncio.gather(*awaitables)
                value = sequence_shape_to_type[field.shape](contents)
            
            v, errors_ = field.validate(value, values, loc=("body", field.alias))
            
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v

    return values, errors
```

This corrected function now properly handles sequence-shaped fields like lists, sets, and tuples in the received body while considering the field's configuration. It extracts values accordingly and processes them based on the field's type and required constraints.

The function should now satisfy all the provided test cases with the expected input/output values and types.