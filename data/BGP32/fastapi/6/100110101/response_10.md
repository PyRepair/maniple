### Analysis:
- The `request_body_to_args` function is responsible for extracting values from a `Dict[str, Any]` or `FormData` object based on the required parameters provided.
- The buggy function seems to have issues handling sequence data types like lists, sets, and tuples properly.
- The failing tests indicate that the function is not extracting the data correctly from the `FormData` object when dealing with sequences.

### Bug:
The bug lies in the way the function handles sequence data types (list, set, tuple) when extracting values from the `FormData` object:
1. The function does not consistently handle extracting sequence data elements from the `FormData` object.
2. It does not properly handle the case when the sequence data is passed inside the `FormData` object.

### Fix Strategy:
To fix the bug and handle sequence data types correctly, we need to:
1. Ensure proper handling of sequence shaped fields.
2. Extract and process sequence data correctly from the `FormData` object.
3. Update the function to account for different sequence data types: list, set, and tuple.

### Corrected Function:
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
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            if (
                field_info := get_field_info(field)
            ) and hasattr(field_info, "embed") and field_info.embed is not None:
                value = {field.alias: value}
            if isinstance(field_info, params.File):
                if lenient_issubclass(field.type_, bytes):
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

Now, the corrected function should correctly handle sequence data types like lists, sets, and tuples when extracting data from the `FormData` object. This fix should address the issues observed in the failing tests and ensure the function works as expected for all cases.