The bug in the `request_body_to_args` function is caused by the incorrect handling of non-typing sequence types like list, set, and tuple in the received body. The function is designed to process the incoming body data based on the specified field shape and type. However, when dealing with non-typing sequence types, the function encounters errors due to the mismatch between the expected and actual data structures.

To fix the bug, we need to adjust the logic in the function to properly handle non-typing sequence types such as list, set, and tuple when extracting values from the received body. Additionally, we should ensure that the values are correctly formatted and stored in the `values` dictionary for further processing.

Below is the corrected version of the `request_body_to_args` function:

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
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)

                if value is None:
                    if field.required:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:
                        values[field.name] = deepcopy(field.default)
                        continue

                if field.shape in sequence_shapes:
                    value = value if isinstance(value, list) else [value]

                if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                    if isinstance(value, list) and all(isinstance(v, UploadFile) for v in value):
                        value = [await v.read() for v in value]
                    elif isinstance(value, UploadFile):
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

The corrected version of the function now properly handles the extraction of values from non-typing sequence types and processes them accordingly. This should allow the function to correctly handle list, set, and tuple data structures when parsing the received body data.

Please test the function with the provided failing test cases to ensure that the bug has been fixed and the function now produces the expected output.