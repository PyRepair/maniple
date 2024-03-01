## Analysis:
1. The function `request_body_to_args` takes a list of required parameters (`required_params`) and the received body data (`received_body`) as input.
2. The function iterates over the required parameters and for each parameter, extracts the value from the received body data using the parameter's alias.
3. It then performs validation on the extracted value based on the parameter's type and shape, adding any errors encountered during validation to the `errors` list.
4. If a value is missing for a required parameter, it adds a `MissingError` to the errors list.
5. There are conditions to handle specific scenarios such as handling file uploads and dealing with sequence shapes.

## Bugs in the Function:
1. The bug lies in the conditional block where the missing value for a required field is being handled.
2. The check `if received_body is not None:` should come before attempting to access `field.alias` and other properties of the field.
3. The logic for checking the shape of the field and extracting the value accordingly is incorrect.

## Bug Fix Strategy:
1. Move the null check for `received_body` to the top of the loop before processing any field.
2. Adjust the logic for extracting the value based on the field's shape and type.
3. Refactor the validation logic to properly handle missing values and generate appropriate error messages.

## Corrected Version of the Function:
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if received_body is not None:
        for field in required_params:
            field_info = get_field_info(field)
            value: Any = None

            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)

            if value is None or (
                isinstance(field_info, params.Form) and value == ""
            ) or (
                isinstance(field_info, params.Form)
                and field.shape in sequence_shapes
                and len(value) == 0
            ):
                if field.required:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
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