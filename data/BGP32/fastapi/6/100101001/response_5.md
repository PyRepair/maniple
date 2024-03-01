The bug in the `request_body_to_args` function lies in the logic to handle non-typing sequences such as lists, sets, and tuples when processing form data. The function is not correctly extracting the values from the FormData object for these cases, leading to errors in validation and incorrect handling of the data.

To fix the bug, we need to adjust the logic for extracting values based on the field type and shape. We should ensure that the values extracted from FormData match the expected data structures (lists, sets, tuples) and handle them accordingly during validation.

Here is the corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        if received_body is not None:
            alias = field.alias
            value = None
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                value = received_body.getlist(alias)
            else:
                value = received_body.get(alias)
            if (
                value is None
                or (isinstance(get_field_info(field), params.Form) and value == "")
                or (
                    isinstance(get_field_info(field), params.Form)
                    and field.shape in sequence_shapes
                    and len(value) == 0
                )
            ):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", alias))
                else:
                    values[field.name] = deepcopy(field.default)
                continue
                
            if (
                isinstance(get_field_info(field), params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif (
                field.shape in sequence_shapes
                and isinstance(get_field_info(field), params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, sequence_types)
            ):
                awaitables = [sub_value.read() for sub_value in value]
                contents = await asyncio.gather(*awaitables)
                value = sequence_shape_to_type[field.shape](contents)
                
            v_, errors_ = field.validate(value, values, loc=("body", alias))
            
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
                
    return values, errors

```

This corrected version ensures proper extraction and handling of values from FormData for non-typing sequences like lists, sets, and tuples, facilitating successful validation and data processing for the failing test cases.