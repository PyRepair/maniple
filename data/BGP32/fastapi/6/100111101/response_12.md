The bug in the `request_body_to_args` function seems to stem from handling values of non-primitive types (like lists, sets, and tuples) in the received body incorrectly, leading to validation errors and an incorrect response status code.

### Cause of the bug:
- The function treats the non-primitive types in the received body as single values while expecting them to be lists or sets for certain field types. This results in validation errors and an HTTP 422 (Unprocessable Entity) status code instead of a successful response.
- The buggy code does not correctly handle non-primitive types like lists, sets, and tuples when parsing the received body.

### Fixing the bug:
To fix the bug, we need to modify the function to correctly handle non-primitive types in the received body, such as lists, sets, and tuples. We should ensure that the values are correctly processed and validated based on their respective types.

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
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    value = received_body.getlist(field.alias)
                else:
                    received_value = received_body.get(field.alias)
                    if received_value is not None:
                        if field.shape in sequence_shapes:
                            # Convert received value to the appropriate type
                            value = sequence_shape_to_type[field.shape](received_value)
                        else:
                            value = received_value
                    else:
                        value = None

            if (
                value is None
                or (isinstance(field_info, params.Form) and value == "")
                or (
                    isinstance(field_info, params.Form)
                    and field.shape in sequence_shapes
                    and len(value) == 0
                )
            ):
                if field.required:
                    if PYDANTIC_1:
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias))
                        )
                    else:
                        errors.append(
                            ErrorWrapper(  # type: ignore
                                MissingError(),
                                loc=("body", field.alias),
                                config=BaseConfig,
                            )
                        )
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

With these corrections, the function should now properly handle non-primitive types in the received body and pass the failing tests.