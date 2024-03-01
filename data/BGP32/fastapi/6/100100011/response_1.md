### Bug Analysis:
1. The `request_body_to_args` function is responsible for converting request body data into arguments for a FastAPI endpoint.
2. The function iterates over the required parameters and retrieves values from the received body data.
3. It validates the retrieved values based on parameter type and shape, handling special cases for files and sequences.

### Bug Location:
The bug might be related to how the function processes sequence-shaped parameters when the received body data is of `FormData` type.

### Cause of the Bug:
1. When processing sequence-shaped fields in the `request_body_to_args` function, the value retrieval logic is incorrect for `FormData` inputs.
2. The logic for getting values for sequence-shaped fields does not handle `FormData` correctly, leading to incorrect values being retrieved or not retrieved at all.

### Bug Fix Strategy:
1. Update the value retrieval logic for sequence-shaped fields to correctly handle `FormData` inputs.
2. Ensure that multiple values for the same key in `FormData` input are processed correctly.

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
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    if field.alias in received_body:  # Check if field alias exists in FormData
                        if field.shape == sequence_shapes[0]:  # Handle list
                            value = received_body.getlist(field.alias)
                        elif field.shape == sequence_shapes[1]:  # Handle set
                            value = set(received_body.getlist(field.alias))
                        elif field.shape == sequence_shapes[2]:  # Handle tuple
                            value = tuple(received_body.getlist(field.alias))
                    else:
                        value = None
                else:
                    value = received_body.get(field.alias)
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
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
                    else:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))
                else:
                    values[field.name] = deepcopy(field.default)
                continue
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

With the corrected logic in place, the `request_body_to_args` function should now correctly process sequence-shaped parameters from `FormData` inputs, allowing the failing tests to pass.