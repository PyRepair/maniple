### Bug Explanation
The buggy function `request_body_to_args` fails to correctly handle repeated keys in form data when dealing with types like `list`, `set`, and `tuple`. This leads to validation issues and incorrect data processing.

In the provided test cases, the functions are expecting to receive a list, set, or tuple of items in the form data, but the current implementation does not properly handle parsing and validating such data structures.

The core issue lies in how the function processes form data with repeated keys and how it validates the input against the expected data types.

### Bug Fix Strategy
To fix this bug and address the GitHub issue, we need to adjust the way the function handles repeated keys in form data and ensure that the correct values are extracted and validated for types like `list`, `set`, and `tuple`.

### Corrected Function
Here is the corrected version of the `request_body_to_args` function that addresses the bug:

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
                    values_list = received_body.getlist(field.alias)
                    if field.type_ in sequence_types:
                        if lenient_issubclass(field.type_, bytes):
                            values_list = [await item.read() for item in values_list]
                        else:
                            values_list = [deserialize_value(field.type_, item) for item in values_list]
                    value = values_list
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

            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_

    return values, errors
```

In this correction, we explicitly handle processing repeated keys from form data, parsing them into lists if necessary, and validating the data against the expected types.

By addressing the way the function deals with repeated keys in form data and ensuring correct processing of list, set, and tuple data structures, the corrected function should pass the failing tests and resolve the GitHub issue related to supporting repeated key=value pairs in form data.