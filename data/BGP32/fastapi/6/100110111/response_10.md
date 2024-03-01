### Analysis
1. The buggy function `request_body_to_args` takes a list of `ModelField` objects and a dict or FormData object as input. It processes the fields and values and validates them. The issue seems to be related to the handling of multiple values for the same key.
2. The error occurs in the processing of repeated keys when the field shape is in `sequence_shapes`. It only retains the last value for the same key instead of collecting all values into a list.
3. The failing tests provide examples where lists, sets, and tuples are not correctly handled when multiple values are sent for the same key. The expected result should be all values combined into a single list, set, or tuple.
4. To fix the bug, we need to modify the logic inside the function to accumulate all values for the same key that are present in FormData objects.
5. The fix should allow proper handling of repeated keys with multiple values in FormData.

### Bug Fix Strategy
1. Locate the portion of code where values for repeated keys are processed.
2. Modify this section to collect all values for the same key into a list, set, or tuple (based on the field type).
3. Ensure that the validation still works correctly after the modification.

### Bug Fixed Version
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
                    if field.alias in received_body:
                        if field.shape == 0:
                            value = [received_body[field.alias]]
                        elif field.shape == 1:
                            value = received_body.getlist(field.alias)
                        elif field.shape == 2:
                            values[field.name] = tuple(received_body.getlist(field.alias))
                        elif field.shape == 3:
                            values[field.name] = set(received_body.getlist(field.alias))
                    elif field.required:
                        if PYDANTIC_1:
                            errors.append(
                                ErrorWrapper(MissingError(), loc=("body", field.alias))
                            )
                        else:  
                            errors.append(
                                ErrorWrapper(
                                    MissingError(),
                                    loc=("body", field.alias),
                                    config=BaseConfig,
                                )
                            )
                    else:
                        values[field.name] = deepcopy(field.default)
                else:
                    value = received_body.get(field.alias) if field.alias in received_body else None
            if value is not None:
                if (
                    isinstance(field_info, params.File)
                    and lenient_issubclass(field.type_, bytes)
                    and isinstance(value, UploadFile)
                ):
                    value = await value.read()
                elif (
                    field.shape in sequence_shapes
                    and isinstance(field_info, params.File)
                    and lenient_issubclass(field.type_, bytes)
                    and isinstance(value, sequence_types)
                ):
                    awaitables = [sub_value.read() for sub_value in value]
                    contents = await asyncio.gather(*awaitables)
                    value = sequence_shape_to_type[field.shape](contents)
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
    return values, errors
```

After fixing the function as shown above, the function should now correctly handle repeated keys in FormData, collect all values for the same key, and return the expected list, set, or tuple. The modified function should pass all the failing tests provided, meeting the expected input/output values and resolving the GitHub issue related to supporting repeated key=value pairs.