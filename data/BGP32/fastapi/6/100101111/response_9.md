### Bug Analysis:
1. The `request_body_to_args` function is supposed to extract values from a received body (either `Dict` or `FormData`) based on the required parameters and their corresponding aliases.
2. The bug occurs when dealing with list, set, and tuple types in the received body. The function fails to properly handle these cases and extract the values correctly.
3. The bug results in the failure of the test functions `test_python_list_param_as_form`, `test_python_set_param_as_form`, and `test_python_tuple_param_as_form`.
4. The bug is related to the GitHub issue titled "Support repeated key=value in form data."

### Bug Fix Strategy:
1. Modify the logic to correctly handle the extraction of list, set, and tuple values from the received body.
2. Ensure that the values are extracted and stored properly before validation.

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
                    value = []
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                if field.shape in sequence_shapes and isinstance(value, sequence_types):
                    awaitables = [sub_value.read() for sub_value in value]
                    contents = await asyncio.gather(*awaitables)
                    value = sequence_shape_to_type[field.shape](contents)
                elif isinstance(value, UploadFile):
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

**Note:** Ensure to update the corresponding imports and dependencies if necessary.