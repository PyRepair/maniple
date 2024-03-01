## Bug Explanation
The buggy function `request_body_to_args` is designed to extract values from the `received_body` for the required parameters specified in `required_params`. The issue arises due to incorrect handling of values when the parameter is a list, set, or tuple.

1. For case 1, when the parameter type is a list, the function should extract the values for the key specified in the alias and create a list of those values.
2. For case 2, when the parameter type is a set, the function should extract the values for the key specified in the alias and create a set of those values.
3. For case 3, when the parameter type is a tuple, the function should extract the values for the key specified in the alias and create a tuple of those values.

The buggy function fails to correctly handle these different parameter types and shapes, leading to errors in extracting and formatting the values.

## Bug Fix Strategy
To fix the bug in the `request_body_to_args` function, we need to modify the value extraction logic based on the shape and type of the field. By correctly handling each type (list, set, tuple), we can ensure that the function extracts and formats the values appropriately.

## Corrected Function
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
                if isinstance(received_body, FormData):
                    value = received_body.getlist(field.alias) if field.shape in sequence_shapes else received_body.get(field.alias)
            if value is None:
                if field.required:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
                    )
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                if (
                    isinstance(field_info, params.File)
                    and lenient_issubclass(field.type_, bytes)
                    and isinstance(value, UploadFile)
                ):
                    value = await value.read()
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
    return values, errors
```

The corrected function now correctly handles extracting values for different parameter types (list, set, tuple) and shapes. The logic has been simplified to ensure proper value extraction and formatting for each field.