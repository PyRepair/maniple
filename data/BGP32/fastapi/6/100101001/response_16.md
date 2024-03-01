### Bug Explanation:
The buggy function `request_body_to_args` is designed to extract values from the received body (either as a dictionary or FormData) based on the required parameters provided. However, the bug lies in how it handles sequences (list, set, tuple) when extracting values from the FormData object. In the current implementation, the function does not handle sequences correctly, resulting in errors when extracting values for these parameters.

### Bug Location:
The bug occurs in the logic that checks for sequence shapes (`sequence_shapes`) and attempts to extract values accordingly from the FormData object. The incorrect handling of sequence shapes leads to errors in the validation process and results in the failing tests.

### Bug Fix Strategy:
To fix the bug, the function needs to properly handle sequences (list, set, tuple) when extracting values from the FormData object. Specifically, the function should iterate over the sequence elements to retrieve and validate each value correctly.

### Corrected Version of the Function:
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
        
        if value is None:
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if field.shape in sequence_shapes and field.alias in received_body.keys():
                if field.shape == 1:
                    value = [received_body.get(field.alias)]
                elif field.shape == 3:
                    value = received_body.getlist(field.alias)
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    
    return values, errors
```

In the corrected version:
- The function iterates over each required parameter and correctly handles sequence shapes when retrieving values from the FormData object.
- It properly validates the extracted values for each field based on its shape and updates the values and errors lists accordingly. 

By implementing these changes, the corrected function should now be able to handle sequences in the FormData object and pass the failing tests successfully.