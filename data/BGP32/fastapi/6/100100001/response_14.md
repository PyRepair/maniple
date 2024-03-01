### Analysis:
The `request_body_to_args` function is intended to convert received body data into arguments based on required parameters. The function iterates through the required parameters, extracts values from the received body, validates them, and populates the `values` dictionary with valid values while accumulating errors in the `errors` list.

Potential errors:
1. Incorrect handling of sequence-shaped parameters.
2. Incorrect handling of different field types such as `params.File`.
3. Improper validation and population of values and errors.

### Bug Description:
The bug in the `request_body_to_args` function lies in the incorrect extraction and processing of sequence-shaped parameters when received data is of type FormData. The current implementation does not handle sequence-shaped parameters properly, leading to incorrect validation and processing of values.

### Bug Fix Strategy:
To fix the bug, focus on improving the handling of sequence-shaped parameters when the received data is of type FormData. Ensure that the values are correctly extracted, validated, and populated into the `values` dictionary while handling errors appropriately.

### Corrected Version of the Function:
Below is the corrected version of the `request_body_to_args` function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    values_list = received_body.getlist(field.alias)
                    value = sequence_shape_to_type[field.shape](values_list)
                else:
                    value = received_body.get(field.alias)
                
                if value is not None:
                    v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                    if isinstance(errors_, ErrorWrapper):
                        errors.append(errors_)
                    elif isinstance(errors_, list):
                        errors.extend(errors_)
                    else:
                        values[field.name] = v_
                else:
                    if field.required:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
                    else:
                        values[field.name] = deepcopy(field.default)
    
    return values, errors
```

In this corrected version, the handling of sequence-shaped parameters from FormData is improved to properly extract values and populate the `values` dictionary. Additionally, errors are handled according to the required parameters.