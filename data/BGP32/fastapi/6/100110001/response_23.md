### Analysis:
- The function `request_body_to_args` is designed to convert request bodies into arguments based on required parameters and received data.
- The failing tests are related to sending arrays (lists, sets, tuples) in the request body.
- The error message indicates that the response status code is 422 (Unprocessable Entity) instead of the expected 200 (OK).

### Potential Errors:
- The function may not handle converting list, set, or tuple types correctly.
- The logic for extracting values from the request body may have issues.
- Validation and error handling for sequences may not be implemented correctly.

### Bug Explanation:
- The function does not correctly handle extracting values for sequence types (lists, sets, tuples) from the request body.
- Due to incorrect handling, the function fails to process the request data and results in a 422 status code response.

### Bug Fix Strategy:
- Update the logic for extracting values from the request body to correctly handle lists, sets, and tuples.
- Validate the extracted values properly and handle errors accordingly to provide the expected response.

### Corrected Function:
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
                if field.shape in sequence_shapes:
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            if value is None or (isinstance(value, list) and len(value) == 0):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
                    continue
            value = value if value is not None else []
            for i, val in enumerate(value):
                if isinstance(field.sub_fields, list) and i < len(field.sub_fields):
                    sub_field = field.sub_fields[i]
                    v_, errors_ = sub_field.validate(val, values, loc=("body", field.alias))
                    if isinstance(errors_, ErrorWrapper):
                        errors.append(errors_)
                    elif isinstance(errors_, list):
                        errors.extend(errors_)
                    else:
                        values[field.name] = v_
                else:
                    values[field.name] = value
    return values, errors
```

### Correction Rationale:
- The corrected function now properly handles extracting values for sequence types by checking if the field shape belongs to sequence shapes.
- Validating values for sub-fields within sequences is added to handle nested structures.
- The function now populates the errors list with error wrappers for missing values or validation errors.

By implementing the corrected function, the issues related to processing sequence types from the request body should be resolved, and the failing tests should pass.