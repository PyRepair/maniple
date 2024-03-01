### Bug Explanation
The bug in the `request_body_to_args` function is related to handling sequence shapes (like lists, sets, and tuples) in the `FormData` input. The function fails to extract the values correctly for sequence-shaped fields when they are represented in the form data.

### Bug Fix Strategy
1. Handle sequence-shaped fields properly in the `FormData` input.
2. Modify the logic to extract and validate values accordingly for each type of sequence.

### Corrected Version of the Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params and received_body:
        for field in required_params:
            value = None
            if field.type_ in sequence_types:  # Check if the field type is a sequence
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

With this corrected version, the function should now correctly handle sequence-shaped fields in the form data, such as lists, sets, and tuples, and pass the failing test cases provided.