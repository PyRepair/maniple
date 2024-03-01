## Bug Fix Strategy:
1. The bug seems to be related to handling repeated keys in form data correctly. The issue description on GitHub confirms this.
2. When processing the form data, the function should handle cases where keys have multiple values correctly.
3. The `getlist` method for FormData is suitable for this scenario as it returns a list of all the values for a given key.
4. The function needs to be modified to extract all values for a key if it appears multiple times in the form data.
5. Ensure that the correct value is assigned to the field in the required_params list.

## The corrected version of the function
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
                    if len(value) == 1:
                        value = value[0]
                else:
                    value = received_body.get(field.alias)

            if value is None or (value == "" and field.required):
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
                values[field.name] = deepcopy(field.default) if not field.required else None
            else:
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

By following the corrected version outlined above, the function now properly handles repeated keys in form data and assigns the correct values to the `values` dictionary. This fix should resolve the failing tests and address the issue reported on GitHub.