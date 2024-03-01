### Bug Explanation
The bug in the `request_body_to_args` function arises from the way it handles multiple values for the same key in the `received_body` FormData. The current implementation does not properly account for repeated keys, leading to validation issues, as observed in the failing tests.

### Bug Fix Strategy
To fix the bug and address the GitHub issue, we need to modify the function to correctly handle multiple values for the same key in the FormData input. The function should aggregate these values into lists before performing validation checks.

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
            value: Any = None
            if isinstance(received_body, FormData):
                if field.shape in sequence_shapes:
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
                
                if isinstance(value, list):
                    if PYDANTIC_1:
                        value = [v.decode() if isinstance(v, bytes) else v for v in value]
                    else:
                        value = [v.decode() if isinstance(v, bytes) else v for v in value]
                    
            if (
                value is None
                or (isinstance(field_info, params.Form) and all([v == "" for v in value]))
            ):
                if field.required:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    values[field.name] = deepcopy(field.default)
                continue
                
            if (
                field.shape in sequence_shapes
                and isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and all([isinstance(v, UploadFile) for v in value])
            ):
                value = [await v.read() for v in value]
                
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    
    return values, errors
```

The corrected version of the function now properly handles multiple values for the same key in the FormData input, aggregating them into lists before validation. This modification aligns with the desired behavior outlined in the GitHub issue.