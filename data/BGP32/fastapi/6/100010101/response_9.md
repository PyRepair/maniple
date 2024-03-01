### Bug Analysis
The bug occurs when handling non-typing sequences like lists, sets, and tuples as form data. The function `request_body_to_args` incorrectly processes received data for these cases, leading to a status code error in the test cases provided.

1. The function checks if the received data is of type `FormData`, and then proceeds to extract values based on the field alias.
2. For sequences such as lists, sets, and tuples, it tries to extract the values by the alias, leading to issues in decoding the elements correctly due to how FormData structures the data.
3. The function does not appropriately handle the conversion of non-typing sequences into their respective types.

### Bug Fix Strategy
To fix the bug, we need to adjust how the function handles non-typing sequences like lists, sets, and tuples in form data. Specifically:
1. For list types, we should ensure that the data extracted is a list.
2. For set types, we should generate a set from the extracted list of elements.
3. For tuple types, we should ensure that the extracted data forms a tuple.

By making these adjustments, we can correctly process the form data and avoid errors in processing non-typing sequences.

### Corrected Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    sequence_shapes = {list, set, tuple}
    sequence_type_mapping = {list: list, set: set, tuple: tuple}
    
    for field in required_params:
        value = None
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                # Extract all values under the field alias
                values_list = received_body.getlist(field.alias)
                # Convert the values list to the appropriate sequence type
                if field.shape in sequence_type_mapping:
                    value = sequence_type_mapping[field.shape](values_list)
            else:
                # Extract single value based on the alias
                value = received_body.get(field.alias)
        
        if value is None or (isinstance(get_field_info(field), params.Form) and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    
    return values, errors
```

By correcting the function to properly extract and handle non-typing sequences in form data, the bug should be fixed. This corrected version should pass the failing test cases provided.