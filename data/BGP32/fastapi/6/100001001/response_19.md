## Bug Explanation

The bug in the `request_body_to_args` function lies in how the function processes the values received in the `received_body` parameter in case of sequence shapes like list, set, or tuple. 

When iterating over the `required_params` to extract values from the `received_body`, the function does not handle sequence shapes correctly. It tries to extract the values by directly accessing the `received_body` with the alias of the field, which works correctly for non-sequence shapes but fails for sequences.

In the failing cases provided:
1. The function does not handle lists correctly, leading to a failure with a `ListError`.
2. The function does not handle sets correctly, leading to a failure with a `SetError`.
3. The function does not handle tuples correctly, leading to a failure with a `TupleError`.

The function should properly extract values for sequence shapes from the `received_body` to avoid these errors.

## Fix Strategy

To fix this bug, we need to adjust how the function extracts values from the `received_body` based on the shape of the field. For sequence shapes like list, set, and tuple, we should handle them appropriately by checking the type and then extracting the values accordingly.

## Corrected Version

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        field = required_params[0]
        field_info = get_field_info(field)
        embed = getattr(field_info, "embed", None)
        if len(required_params) == 1 and not embed:
            received_body = {field.alias: received_body}

        for field in required_params:
            value: Any = None

            if received_body is not None:
                if isinstance(received_body, FormData):
                    if field.shape in sequence_shapes:
                        if field.alias in received_body:
                            # Extract values for sequence shapes
                            if field.shape == 1:  # list
                                value = received_body.getlist(field.alias)
                            elif field.shape == 2:  # set
                                value = set(received_body.getlist(field.alias))
                            elif field.shape == 3:  # tuple
                                value = tuple(received_body.getlist(field.alias))
                        else:
                            value = None
                    else:
                        value = received_body.get(field.alias)

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

            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes) and isinstance(value, UploadFile):
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

This corrected version of the `request_body_to_args` function includes handling for sequence shapes when extracting values from the `received_body`. It checks the shape of the field and appropriately extracts the values as lists, sets, or tuples to prevent errors and ensure correct function behavior.