### Analysis:
- The `request_body_to_args` function is responsible for extracting values from the received body based on the required parameters.
- The main issue seems to be related to how the function handles different shapes of parameters (like lists, sets, tuples) and values in the received body.
- The failing tests indicate that the function is returning a status code of 422 (unprocessable entity) instead of the expected status code of 200 for successful extraction of parameters from the body.

### Bug:
- The bug seems to be in how the function is handling iterable elements like lists, sets, and tuples within the received body.
- It fails to properly extract these values and assign them to the corresponding parameters, leading to validation errors and the wrong HTTP status code in the response.

### Fix Strategy:
1. Update the function to correctly handle different shapes of parameters and interpreting values within the received body.
2. Ensure that the extraction and validation process is done correctly for all types of iterable elements.
3. Properly construct the `values` dictionary with the extracted values and handle any errors in the process.

### Correction:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value = None
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
        
        if value is None or value == "":
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
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

By correcting how the function deals with iterable elements and validates the extracted values, the function should now correctly handle the required parameters and return the expected values for each test case.