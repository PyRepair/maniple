### Analysis:
1. The `request_body_to_args` function is used to convert request body data into arguments based on the specified required parameters.
2. The function iterates over required parameters, extracts corresponding values from the received body, handles file uploads, validates the values, and populates the `values` dictionary while collecting any errors encountered.
3. The failing tests are related to sending data with Python list, set, and tuple parameters to the server and checking if the response status code is 200 and if the response data matches the expected data.
4. The primary cause of the bug seems to be the handling of sequence types in the request body. The function incorrectly processes values for list/set/tuple data in the request body, leading to validation errors and status code 422 in the tests.

### Bug Fix Strategy:
1. We need to ensure that the function correctly handles sequence types like lists, sets, and tuples in the request body data.
2. Specifically, for sequence types, we should extract values using the field alias and handle them appropriately based on their type (string, list, set, tuple).
3. Updating the logic to account for the correct treatment of sequence data for the specified parameters will likely resolve the bug.

### Corrected Version of the Function:
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
                value = received_body.get(field.alias)
                if value is not None:
                    if isinstance(field, ModelField) and field.sub_fields:
                        # Handle sequence shapes
                        values[field.name] = []
                        for elem in value:
                            for sub_field in field.sub_fields:
                                sub_value = elem.get(sub_field.alias)
                                v_, errors_ = sub_field.validate(sub_value, values, loc=("body", sub_field.alias))
                                if isinstance(errors_, ErrorWrapper):
                                    errors.append(errors_)
                                elif isinstance(errors_, list):
                                    errors.extend(errors_)
                                else:
                                    values[field.name].append(v_)
                    else:
                        v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                        if isinstance(errors_, ErrorWrapper):
                            errors.append(errors_)
                        elif isinstance(errors_, list):
                            errors.extend(errors_)
                        else:
                            values[field.name] = v_
            else:
                if field.required:
                    if PYDANTIC_1:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))
                else:
                    values[field.name] = deepcopy(field.default)
    return values, errors
```

In the corrected version, we handle sequence shapes correctly by iterating over elements and extracting values for each subfield. This modification ensures that data in lists, sets, and tuples are extracted and validated properly, addressing the issue causing the failing tests.