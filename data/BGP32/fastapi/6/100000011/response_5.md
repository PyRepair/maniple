### Analysis:
The buggy function `request_body_to_args` is responsible for converting received body data into arguments according to the required parameters. The issue on GitHub suggests that the function should be able to handle repeated key=value pairs in form data and assign those values as a list to the same key before validation.

### Potential Error Location:
1. Handling repeated key=value pairs in form data.
2. Incorrectly assigning values to the keys in the case of sequence shapes.

### Cause of the Bug:
The current implementation of the function does not handle repeated key=value pairs effectively when dealing with FormData. This results in only the last value being considered for a given key. Additionally, the handling of values for keys in sequence shapes is not optimal, leading to incorrect assignment of values to the keys.

### Fix Strategy:
To fix the bug, we need to modify the function to handle repeated key=value pairs correctly, store these values as lists for the same key, and ensure proper assignment of values for keys in sequence shapes.

### Corrected Version:
Here is the corrected version of the `request_body_to_args` function:

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
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            if (
                value is None
                or isinstance(field_info, params.Form) and not value
                or field.shape in sequence_shapes and not value
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

In this corrected version, the function now correctly handles repeated key=value pairs in the case of FormData. It uses `getlist` method to retrieve the list of values for a repeated key. Additionally, the assignment of values to keys in sequence shapes has been improved for better validation.