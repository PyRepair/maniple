### Bug Explanation
The buggy function `request_body_to_args` is designed to handle mapping of request body parameters to corresponding values based on the required parameters. However, there are multiple issues causing the failing tests.

1. The function does not properly handle the case when a single parameter is provided in the request body, resulting in incorrect reassignment of `received_body`.
2. The validation process for different parameter types like `list`, `set`, and `tuple` is not correctly implemented, leading to errors in validation logic.

### Bug Fix Strategy
To fix the bug, we need to:
1. Update the logic for handling single required parameter cases where reassigning `received_body` should be avoided.
2. Correctly validate different parameter types (`list`, `set`, `tuple`) based on their expected shapes without causing errors.

### Corrected Function
Here is the corrected version of the `request_body_to_args` function:

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
            if isinstance(received_body, FormData):
                value = received_body.getlist(field.alias) if field.shape == 1 else received_body.get(field.alias)
        
        if value is None:
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if isinstance(field.field_info, params.File) and lenient_issubclass(field.type_, bytes):
                if isinstance(value, UploadFile):
                    value = await value.read()
                elif isinstance(value, sequence_types):
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

By implementing the corrected fix, the `request_body_to_args` function should now correctly handle the validation and mapping of different parameter types and resolve the failing tests.