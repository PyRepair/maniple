### Bug Explanation:
The bug in the `request_body_to_args` function is related to how the function handles non-typing sequences like lists, sets, and tuples from the request body. The function fails to correctly process these non-typing sequences, leading to errors and incorrect values being returned. The cases provided indicate issues with handling these non-typing sequences when extracting values from the request body.

### Bug Location:
The bug is primarily located in the section where the function attempts to extract values from the request body for non-typing sequences. Specifically, the logic for getting values for different field shapes (e.g., list, set, tuple) is causing the issue.

### Bug Fix Strategy:
To fix the bug, we need to update the logic for processing non-typing sequences in the request body. We should handle lists, sets, and tuples differently based on their data types and shapes. Additionally, handling for different field shapes needs to be improved to correctly extract values for non-typing sequences.

### Corrected Version of the Function:
```python
# Import required libraries

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
                    if field.shape == 1:  # List
                        value = received_body.getlist(field.alias)
                    elif field.shape == 3:  # Set
                        value = set(received_body.getlist(field.alias))
                    elif field.shape == 4:  # Tuple
                        value = tuple(received_body.getlist(field.alias))

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
                    else:  # pragma: nocover
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
            if (
                isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                if isinstance(value, UploadFile):
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

### Proposed Changes:
1. Updated the logic for handling non-typing sequences based on the shape (list, set, tuple).
2. Correctly extract values for different shapes of non-typing sequences from the request body.
3. Ensure that the validation and processing steps handle list, set, and tuple values appropriately.

By making these adjustments, the corrected function should now be able to handle non-typing sequence values correctly, allowing the tests to pass successfully.