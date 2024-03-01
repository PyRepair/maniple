### Analysis:
1. The `request_body_to_args` function is intended to convert request body parameters into a dictionary of values and a list of errors based on the required parameters.
2. The function iterates over the required parameters, extracts values from the received body, validates them, and populates a dictionary with the valid values and a list of errors for invalid or missing values.
3. The bug likely occurs due to incorrect handling of sequence shapes like lists, sets, and tuples when processing form data.
4. The failing tests indicate that the function currently does not correctly handle sequences like lists, sets, and tuples as form data, leading to incorrect output and validation errors.

### Bug:
The bug occurs when processing form data with repeated keys, where the function does not handle repeated keys correctly, resulting in incorrect values and errors. The function's logic for extracting values and processing sequences is flawed, leading to validation errors and inconsistencies with expected behavior for form data with repeated keys.

### Bug Fix Strategy:
1. Adjust the logic for handling repeated keys in form data to properly collect them as a list of values for a single key.
2. Update the handling of different sequence shapes to ensure proper extraction and processing of values for lists, sets, and tuples.
3. Refactor the way sequence shapes are validated and processed within the function to align with the expected behavior and handle form data inputs correctly.

### Corrected Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []

    if required_params and received_body is not None:
        for field in required_params:
            value: Any = None

            if isinstance(received_body, FormData):
                values_list = received_body.getlist(field.alias)
                if len(values_list) == 1:
                    value = values_list[0]
                else:
                    value = values_list

            if value is None or (isinstance(get_field_info(field), ModelField) and value == ""):
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
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

The corrected function addresses the bug by ensuring correct handling of repeated keys in form data, extracting values for different sequence shapes, and validating the extracted values properly. This correction aligns the function's behavior with the expected input/output values and resolves the issue raised on GitHub regarding support for repeated keys in form data.