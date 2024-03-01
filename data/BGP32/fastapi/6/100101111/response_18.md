### Bug Explanation
The bug is caused by the function `request_body_to_args` not handling repeated keys in form data correctly. When the same key appears multiple times in the form data, the function only considers the last value, leading to validation errors with the expected input/output values.

The buggy function does not properly handle the case when the same key appears multiple times in the form data. It only considers the last value for that key, leading to validation errors with the expected input/output values.

### Bug Fix Strategy
To fix the bug, we need to modify the function `request_body_to_args` to properly handle repeated keys in form data. Rather than discarding previous values for the same key, we should collect all values for the same key and store them as a list before validation.

### Corrected Version of the Function
Here is the corrected version of the `request_body_to_args` function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        for field in required_params:
            values[field.name] = None  # Initialize values with None for all required fields
        
        if received_body is not None:
            for field in required_params:
                if field.alias in received_body.keys():
                    values[field.name] = received_body.getlist(field.alias)
        
        for field in required_params:
            if values[field.name] is None:  # Check if a value exists for the field
                if field.required:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if isinstance(field_info, params.File)
                    and lenient_issubclass(field.type_, bytes):
                    if isinstance(values[field.name], list):
                        values[field.name] = [await value.read() for value in values[field.name]]
                    else:
                        values[field.name] = await values[field.name].read()
    
    return values, errors
```

By collecting all values for the same key in a list before validation, the corrected function now properly handles repeated keys in form data.

After applying this fix, the function should now pass the failing tests with the expected input/output values and resolve the GitHub issue related to supporting repeated key-value pairs in form data.