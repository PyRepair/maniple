### Cause of the Bug
The bug in the `request_body_to_args` function arises from the way it processes the incoming `FormData` when dealing with non-typing sequences like lists, sets, and tuples. It incorrectly tries to extract the values using the alias of the field, leading to errors in validation for required parameters and shaping the final values.

The key issue can be summarized as follows:
- When dealing with non-typing sequence fields and `FormData`, the function does not correctly handle the extraction of values from the `FormData`.
- It erroneously tries to obtain the values by the alias of the field, causing mismatched values during processing.
- This incorrect handling leads to validation errors and incorrect values being assigned to the fields in the final dictionary.

### Fix Strategy
To fix this bug, the function needs to be revised to properly handle extracting values for non-typing sequence fields such as lists, sets, and tuples from the incoming `FormData`. We should ensure that the correct values are extracted and validated based on the field's actual type and structure.

### Corrected Version of the Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    for field in required_params:
        if isinstance(field.type_, list) or isinstance(field.type_, set) or isinstance(field.type_, tuple):
            if received_body is not None:
                value = received_body.get(field.alias)
                if value is not None:
                    if isinstance(value, list) or isinstance(value, set) or isinstance(value, tuple):
                        value = list(value)  # Convert to list for consistent handling
                    else:
                        value = [value]  # Wrap single value in a list for consistency
                    values[field.name] = value
                else:
                    if field.required:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:
                        values[field.name] = deepcopy(field.default)
        else:
            value = None
            if received_body is not None:
                value = received_body.get(field.alias)
            if value is None:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
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

By making these modifications, the corrected function now properly handles extracting values for non-typing sequences from the `FormData` while ensuring correct validation and error handling based on field types. This should address the issues seen in the failing tests and provide the expected results.