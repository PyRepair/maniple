### Analysis:
1. The `request_body_to_args` function is responsible for converting a request body into arguments based on the required parameters provided.
2. The function checks the required parameters and processes them based on their types and shapes.
3. The failing tests are related to posting data for Python list, set, and tuple parameters, but the function is returning a 422 status code instead of the expected 200, indicating that there is an issue with processing the request body into arguments.
4. The issue seems to be related to how the function processes different types of sequence-shaped fields (list, set, tuple).
5. The function is not handling the sequence-shaped fields correctly, leading to validation errors and incorrect results.

### Bug Cause:
1. The function is not properly handling the `sequence_shapes` in the input data, causing errors to be appended to the `errors` list.
2. The function does not correctly validate the received data for sequence-shaped fields like lists, sets, and tuples, leading to the incorrect status code in the failing test.

### Bug Fix:
1. The bug can be fixed by updating the way sequence-shaped fields are processed, ensuring correct validation and handling of different sequence types.
2. We need to properly handle the sequence shapes to ensure that the data is correctly validated and processed.

### Corrected Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    sequence_shapes = {tuple, list, set}

    for field in required_params:
        alias = field.alias
        if received_body is not None:
            value = received_body.get(alias)
            if value is not None:
                if field.shape in sequence_shapes:
                    if isinstance(value, list):
                        value = field.type_(value)
                    else:
                        value = field.type_(value.split(","))
                try:
                    v_, errors_ = field.validate(value, values, loc=("body", alias))
                    if isinstance(errors_, ErrorWrapper):
                        errors.append(errors_)
                    elif isinstance(errors_, list):
                        errors.extend(errors_)
                    else:
                        values[field.name] = v_
                except Exception as e:
                    errors.append(ErrorWrapper(e, loc=("body", alias)))

            else:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", alias))
                else:
                    values[field.name] = deepcopy(field.default)                

    return values, errors
```

### Explanation of Correction:
1. The corrected function properly handles sequence-shaped fields by checking the received data for different types (list, set, tuple).
2. It validates and processes the data based on the type and shape of the field, ensuring correct conversion and validation.
3. The function now correctly validates the data for sequence-shaped fields and populates the values and errors list accordingly.

By applying these corrections, the `request_body_to_args` function should now correctly process the input data for sequence-shaped fields and pass the failing tests successfully.