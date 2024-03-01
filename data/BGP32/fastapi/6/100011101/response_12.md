### Bug Explanation:
The buggy function `request_body_to_args` is not properly handling non-typing sequences (lists, sets, tuples) passed as form data. The issue arises from how it processes the received data and constructs the values to be returned.

In each failing test case, the function incorrectly handles the non-typing sequence data in the form. It attempts to get the value for the field alias directly, which works for singular values but fails for sequences like lists, sets, and tuples.

The function fails to correctly process the sequence shapes and instead treats them as singular values, resulting in the MissingError being appended to the errors list due to the incorrect parsing of sequence items.

### Bug Fix Strategy:
To fix this bug:
1. Check if the received_body contains a list of values for the specified field alias.
2. If the field shape is a sequence and the received_body is of type FormData, extract the list of values using `getlist()` method instead of `get()`.
3. Update the values dictionary to correctly store the sequence values under the field name.
4. Handle different sequence shapes and types as required by the field information.
5. Ensure that the validation properly processes the extracted values from the form data.

### Corrected Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value: Any = None
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
            
        if value is None or len(value) == 0:
            if field.required:
                if PYDANTIC_1:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                value = await asyncio.gather(*[v.read() for v in value]) if isinstance(value, sequence_types) else await value.read()
            
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    
    return values, errors
```

By modifying the function to handle sequence shapes correctly and extracting the list values where needed, the corrected version should process the form data, including non-typing sequences, more accurately and pass the failing tests.