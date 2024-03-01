### Analysis
1. The `request_body_to_args` function processes required parameters and received data to extract values for the parameters and handle any errors that occur during validation.
2. The function iterates over each required parameter and attempts to extract the corresponding value from the received body data.
3. The issues causing the failures in the test cases are related to how the function handles sequence shapes like lists, sets, and tuples when the received data is a FormData object.
4. The function does not correctly handle FormData inputs for sequence shapes, leading to errors in validation and causing the test failures.

### Bug Explanation
The buggy function `request_body_to_args` fails to correctly map received data from a FormData object to values in cases where the parameter's shape is a list, set, or tuple. This leads to validation errors and incorrect handling of the received data.

In the failing tests:
1. The function does not correctly extract a list from FormData in the `test_python_list_param_as_form` test, causing a status code mismatch error.
2. Similarly, in the `test_python_set_param_as_form` test, the function fails to extract and format a set correctly from FormData, leading to a status code mismatch.
3. The function fails to extract tuple data properly from FormData, leading to a status code mismatch in the `test_python_tuple_param_as_form` test.

### Bug Fix Strategy
To fix the bug, the function `request_body_to_args` needs to properly handle the extraction of list, set, and tuple data from FormData. Specifically, the function should handle these cases separately to correctly convert the received data into the expected format for each shape.

### Corrected Function
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
                if field.alias in received_body:
                    value = received_body.get(field.alias)

                if value is not None:
                    if lenient_issubclass(field.type_, list):
                        value = value if isinstance(value, list) else [value]
                    elif lenient_issubclass(field.type_, set):
                        value = set(value if isinstance(value, list) else [value])
                    elif lenient_issubclass(field.type_, tuple):
                        value = tuple(value if isinstance(value, list) else [value])

            if value is None:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
                else:
                    values[field.name] = deepcopy(field.default)
                continue

            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                if isinstance(value, UploadFile):
                    value = await value.read()

            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_

    return values, errors
```

By making the changes outlined in the corrected function, the `request_body_to_args` function should be able to handle FormData inputs correctly for sequence shapes like lists, sets, and tuples. The function should now pass the failing tests with the expected input/output values provided in the cases.