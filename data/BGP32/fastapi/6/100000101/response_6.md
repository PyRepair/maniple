The bug in the provided function lies in the logic used to handle the values extracted from the `received_body` when it is a `FormData` object. The current implementation does not correctly handle the cases where the field shape is a sequence (like list, set, tuple) and the received value needs to be transformed accordingly.

To fix this bug, we need to modify the logic to properly handle sequences when extracting values from `received_body`.

Here is the corrected version of the function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    for field in required_params:
        field_info = get_field_info(field)
        field_alias = field.alias
        value: Any = None

        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                values_list = received_body.getlist(field_alias)
                if field.type_ == set:
                    value = set(values_list)
                elif field.type_ == tuple:
                    value = tuple(values_list)
                else:  # default to list
                    value = values_list
            else:
                value = received_body.get(field_alias)
                
        if value is None or (field.required and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field_alias))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
                value = await value.read()
            elif field.shape in sequence_shapes and isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, sequence_types):
                awaitables = [sub_value.read() for sub_value in value]
                contents = await asyncio.gather(*awaitables)
                
                if field.type_ == set:
                    value = set(contents)
                elif field.type_ == tuple:
                    value = tuple(contents)
                else:  # default to list
                    value = contents
            
            v_, errors_ = field.validate(value, values, loc=("body", field_alias))
            
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_

    return values, errors
```

This corrected function now handles the scenario when the received values in a `FormData` object need to be transformed into sequences like lists, sets, or tuples based on the field type. It ensures correct extraction and validation of values based on the field requirements and shapes.

Please test this corrected version with the expected input/output values provided in the test cases to validate its functionality.