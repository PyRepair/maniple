### Bug Explanation
The bug in the `request_body_to_args` function arises from the incorrect handling of sequence-shaped fields (such as lists, sets, or tuples) when processing the `received_body` input. The function fails to properly evaluate the values based on the shape of the field and ends up generating errors when validating the data.

### Bug Location
The main issue occurs in the section where the function checks for sequence-shaped fields and attempts to extract values from the `received_body` based on the field's alias.

### Bug Fix
To fix this bug, you need to modify the logic that handles sequence-shaped fields within the loop. Specifically, you need to adjust how the values are extracted from the `received_body` and correctly handle the validation of these values.

### Corrected Version of the Function

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    for field in required_params:
        alias = field.alias
        value: Any = None
        
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if isinstance(field.type_, type) and issubclass(field.type_, Sequence):
                    value = received_body.getlist(alias)
                else:
                    value = received_body.get(alias)
            else:
                value = received_body.get(alias)
                
        if (
            value is None
            or (isinstance(field.shape, type) and issubclass(field.shape, (list, tuple, set)) and len(value) == 0)
        ):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", alias))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            v_, errors_ = field.validate(value, values, loc=("body", alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_

    return values, errors
```

In this corrected version:
- We removed the unnecessary handling of the `received_body` within the loop.
- Improved the logic for extracting values from `received_body` based on the field's shape and type.
- Adjusted the validation process to handle sequence-shaped fields properly.
- Updated the handling of errors and value assignments for each field.