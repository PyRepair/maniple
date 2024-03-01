### Bug Explanation:
The bug in the `request_body_to_args` function lies in the handling of input data for sequence types such as lists, sets, and tuples. The function incorrectly processes the received body data when the required parameter is a sequence, leading to errors in the validation process.

### Bug Location:
The bug mainly arises from how the function interacts with the `received_body` data when dealing with sequence shapes.

### Bug Fix Strategy:
1. Update the logic for extracting values from `received_body` based on whether it is a sequence or not.
2. Validate the extracted values appropriately before assigning them to the `values` dictionary.
3. Ensure that the validation and error handling logic is correctly applied to all cases.

### Corrected Version of the Function:
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
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if not isinstance(field.type_, type):
                    field_type = field.type_.__args__[0]
                else:
                    field_type = field.type_
                    
                if field_type == list:
                    value = received_body.getlist(field.alias)
                elif field_type == set:
                    value = set(received_body.getlist(field.alias))
                elif field_type == tuple:
                    value = tuple(received_body.getlist(field.alias))
                else:
                    value = received_body.getlist(field.alias)

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
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig)
                    )
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

The corrected version of the function now correctly handles the extraction of values from `received_body` based on the sequence type specified by the required parameter. This version aligns the processing logic with the expected behavior for lists, sets, and tuples, ensuring successful validation and error handling.