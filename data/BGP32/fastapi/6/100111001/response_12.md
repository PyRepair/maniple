### Bug Analysis:
The buggy function `request_body_to_args` is designed to convert incoming request body data into arguments. It processes the required parameters and values stored in the request body. The bug arises from how it handles certain types of parameters such as sets, lists, and tuples. The function incorrectly processes these non-typing sequences, leading to validation errors and incorrect responses.

In each test case, the required parameter `items` is passed with values `["first", "second", "third"]` as a list, set, and tuple respectively. The function tries to process these values within the `received_body`, which leads to the conversion errors and responses with status code 422 instead of the expected 200.

### Bug Cause:
1. The function fails to check the correct conditions for handling sequence shapes when extracting values from the `received_body`.
2. There is a discrepancy between the expected types of parameters and how the values are processed, leading to validation errors and incorrect responses.

### Bug Fix Strategy:
1. Modify the code to correctly handle different sequence shapes (lists, sets, tuples) within the `received_body`.
2. Ensure that validations are done based on the correct parameter types to prevent errors in processing the received data.
3. Fix the conditions that check for required parameters and skip non-required ones appropriately.

### Corrected Function:
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
            if field.alias in received_body:
                if field.shape in sequence_shapes and isinstance(
                    received_body[field.alias], list
                ):
                    value = received_body[field.alias]
                else:
                    value = received_body[field.alias]

        if value is None or (isinstance(field_info, params.Form) and value == "") or (
            isinstance(field_info, params.Form)
            and field.shape in sequence_shapes
            and len(value) == 0
        ):
            if field.required:
                if PYDANTIC_1:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))
            else:
                values[field.name] = deepcopy(field.default)
            continue

        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_

    return values, errors
```

### Summary:
By correcting the handling of different sequence shapes and ensuring proper validation based on parameter types, the corrected function should now process the request body data accurately. This should resolve the validation errors and ensure that the function returns the expected responses for the provided test cases.