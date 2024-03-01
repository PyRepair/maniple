### Bug Explanation
The buggy function `request_body_to_args` is not handling repeated keys in form data correctly. When there are multiple values for the same key, the function only considers the last one instead of collecting all values into a list. This leads to validation issues and incorrect results during form data processing.

### Bug Location
The bug is primarily located in the section where the function extracts values from `received_body` and assigns them to the corresponding fields. Specifically, when dealing with values in a sequence form (e.g., list, set, tuple), the function fails to process multiple values for the same key correctly.

### Bug Cause
The cause of the bug is the lack of handling multiple values for the same key in form data. The function incorrectly assumes a single value for each key, which leads to errors when dealing with sequences like lists, sets, and tuples.

### Strategy for Fixing the Bug
To fix the bug, the function needs to check if a key has multiple values and collect them into a list for processing. This involves updating how the function extracts values from `received_body`, especially for fields that have sequence shapes.

### Corrected Version of the Function
Here is the corrected version of the `request_body_to_args` function:

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
                        value = received_body.getlist(field.alias)
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

In this corrected version, the function properly handles keys with multiple values by checking if the key exists in the form data and collecting all values into a list for further processing. This fix addresses the issue described in the failing tests and aligns with the desired behavior outlined in the GitHub issue about supporting repeated key=value pairs in form data.