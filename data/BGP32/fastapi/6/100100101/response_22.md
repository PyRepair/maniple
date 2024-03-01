## Bug Explanation
The bug in the `request_body_to_args` function arises from how the function handles non-typing sequence shapes (list, set, tuple) when processing request body values. The bug causes incorrect handling of non-typing sequence shapes, leading to incorrect validation and data extraction from the received body.

The main issue arises from the incorrect handling of non-typing sequence shapes in the function. The function does not correctly process values for `list`, `set`, and `tuple` types when extracting them from the request body. This results in error-prone behavior and incorrect data extraction.

## Bug Fix Strategy
To fix the bug, the function needs to properly handle non-typing sequence shapes like `list`, `set`, and `tuple` when extracting values from the request body. The function should differentiate between these sequence shapes and process their values accordingly. Additionally, the bug fix should ensure that the validation and extraction process align with the expected behavior for non-typing sequence shapes.

## Bug-Fixed Function

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        for field in required_params:
            field_info = get_field_info(field)
            embed = getattr(field_info, "embed", None)
            value: Any = None
            
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            
            if (value is None or 
               (isinstance(field_info, params.Form) and value == "") or
               (isinstance(field_info, params.Form) and field.shape in sequence_shapes and len(value) == 0)):
                
                if field.required:
                    missing_location = "query" if isinstance(field_info, params.Query) else "body"
                    errors.append(ErrorWrapper(MissingError(), loc=(missing_location, field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if field.shape in sequence_shapes and isinstance(field_info, params.AbstractSet):
                    value = sequence_shape_to_type[field.shape](value)
                elif field.shape in sequence_shapes and isinstance(field_info, params.AbstractTuple):
                    value = tuple(value)
                    
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

This corrected version of the `request_body_to_args` function addresses the incorrect handling and extraction of non-typing sequence shapes from the request body. It correctly processes values for list, set, and tuple types and aligns with the expected behavior for such data structures.