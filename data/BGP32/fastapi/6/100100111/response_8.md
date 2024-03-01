### Analysis:
1. The `request_body_to_args` function is designed to convert request body data (received as a dict or FormData) into parameters required by the function. It processes the received body data based on the required parameters provided.
2. The bug occurs when handling sequences in the body data, specifically handling lists, sets, and tuples while validating the data against the required parameters.
3. The bug prevents the function from correctly detecting and handling sequences like lists, sets, and tuples, which results in incorrect validation and processing of the data.
4. To fix the bug, the function needs to be modified to correctly handle sequences in the received body data and map them to the required parameters.

### Bug Explanation:
- The bug arises from the incorrect processing of sequence-shaped field data (like lists, sets, or tuples) when validating against the required parameters.
- In the provided function, the logic for processing sequences is not handling them appropriately, leading to errors in validation and assignment of values to parameters.
- Due to the improper handling of sequences, the function fails to pass the tests for lists, sets, and tuples being passed as form data.

### Fix Strategy:
1. Check if the received body data contains sequences and handle them accordingly.
2. Process the sequences appropriately based on the required parameter type (list, set, or tuple).
3. Ensure that the values extracted from the received body data are correctly mapped to the required fields for further validation.

### Updated Corrected Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        field_info = get_field_info(required_params[0])
        embed = getattr(field_info, "embed", None)
        
        # Handle embedded single field without embed attribute
        if len(required_params) == 1 and not embed:
            received_body = {field.alias: received_body}
        
        for field in required_params:
            value: Any = None
            
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    values[field.name] = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            
            if value is None or (isinstance(field_info, params.Form) and value == "") or (isinstance(field_info, params.Form) and field.shape in sequence_shapes and len(value) == 0):
                if field.required:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
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

By updating the logic to correctly handle sequences in the received body data, the corrected function should now pass the failing tests and correctly validate form data containing lists, sets, and tuples.