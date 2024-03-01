The issue in the `request_body_to_args` function stems from how it handles non-typing sequences (`list`, `set`, `tuple`) in the `received_body` parameter. The function incorrectly assumes that it can directly access the values associated with the specified field alias without considering the shape of the parameter. This leads to errors when processing sequences that are not individual field values.

To fix the bug, we need to update the function to properly handle non-typing sequences in the `received_body`. We should extract the full sequence associated with the field and process it accordingly. Here is the corrected version of the function:

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
                    if field.shape in sequence_shapes:
                        values_list = received_body.getlist(field.alias)
                        value = values_list if values_list else None
                    else:
                        value = received_body.get(field.alias)

            if value is None and field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            elif value is None:
                values[field.name] = deepcopy(field.default)
            else:
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_

    return values, errors
```

This updated function now correctly processes non-typing sequences in the `received_body` parameter like lists, sets, and tuples. By checking the shape of the field, it can extract the complete sequence associated with the alias before validation and storing the values in the result dictionary.

This corrected function should now pass the failing tests for processing non-typing sequences in the fastapi dependency context.