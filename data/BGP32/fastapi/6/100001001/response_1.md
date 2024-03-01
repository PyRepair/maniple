### Explanation:
The bug in the `request_body_to_args` function seems to stem from how the function handles fields with sequence types (`list`, `set`, `tuple`) when parsing the received body data. In each case provided, the function incorrectly processes the input data due to how it handles sequence shapes and the received body format.

1. The function iterates over `required_params` and retrieves the `value` from the `received_body` based on the field's `alias`. However, it doesn't handle sequences properly, leading to errors and incorrect values being processed.

2. There are multiple issues in the code related to the handling of sequence shapes and the interactions between field types and received body data. This results in wrong values being processed and errors being incorrectly raised.

### Strategy for Fixing the Bug:
To fix the bug in the `request_body_to_args` function, we need to adjust how the function handles fields with sequence shapes and correctly extracts values from the received body data, considering the field types.

### Correction to the Buggy Function:
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
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.shape == 2:  # If sequence shape is set or tuple
                    value = (received_body.get(field.alias),)
                else:
                    value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
                
        if value is None or (isinstance(field_info, params.Form) and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
        else:
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                if isinstance(value, UploadFile):
                    value = await value.read()
                elif field.shape in sequence_shapes and isinstance(value, sequence_types):
                    awaitables = [sub_value.read() for sub_value in value]
                    contents = await asyncio.gather(*awaitables)
                    if field.shape == 3:  # List of files (bytes) in this context
                        value = contents
                    else:  # Unexpected shape, set the field value to the error
                        value = None
            
            if value is not None:
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_

    return values, errors
```

In the corrected function, I've included specific checks for the different sequence shapes (`list`, `set`, `tuple`) and adjusted the logic for handling these cases properly. This should address the issues with extracting values from the received body data and ensure correct processing of the fields.