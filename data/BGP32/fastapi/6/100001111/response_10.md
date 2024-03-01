Based on the provided information, the bug in the `request_body_to_args` function stems from how it handles multiple values for the same key in the `received_body` parameter. The function currently does not aggregate these values correctly when dealing with sequences like lists, sets, or tuples.

To resolve this bug and address the GitHub issue regarding supporting repeated key=value pairs in form data, we need to modify the logic where the function processes the values from the `received_body` parameter.

Here is a corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if received_body is not None:
        for field in required_params:
            value: Any = None
            
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                raw_values = received_body.getlist(field.alias)
                
                if field.type_ == list:
                    value = raw_values
                elif field.type_ == set:
                    value = set(raw_values)
                elif field.type_ == tuple:
                    value = tuple(raw_values)
            else:
                value = received_body.get(field.alias) if received_body.get(field.alias) else None
                
            if value is None or (isinstance(field_info, params.Form) and value == "") or (
                isinstance(field_info, params.Form) and field.shape in sequence_shapes and len(value) == 0
            ):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if isinstance(value, UploadFile):
                    value = await value.read()
                elif field.shape in sequence_shapes and isinstance(value, sequence_types):
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

This corrected version of the function properly handles multiple values for the same key in the `FormData` input, aggregating them based on the field type (list, set, tuple) specified in the `ModelField`.

By making these changes, the function now aligns with the expected input/output values and addresses the underlying bug while also supporting the desired feature outlined in the GitHub issue.