## Bug Explanation
The bug in the `request_body_to_args` function lies in how FormData is handled when passed with sequences like lists, sets, and tuples. The function is currently treating each element of the sequence as a separate value in FormData, which leads to incorrect parsing and validation, causing the function to return errors instead of the expected values.

- In Case 1 (list parameter):
  - The function treats each item in the list as a separate value in the FormData, resulting in errors as the validation expects a single list, not separate values.

- In Case 2 (set parameter):
  - The behavior is similar to Case 1, treating each item as a separate value in the FormData and leading to errors during validation.

- In Case 3 (tuple parameter):
  - The function erroneously converts the tuple into a list of elements in the FormData, causing validation errors when attempting to validate the tuple.

## Fix Strategy
To fix the bug, the function should properly handle sequences like lists, sets, and tuples when passed as parameters. The function needs to correctly interpret the FormData to extract the entire sequence as a single value for validation.

## Corrected Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params and received_body is not None:
        for field in required_params:
            value = None
            if field.alias in received_body:
                value = received_body.get(field.alias)
            if value is None and field.required:
                errors.append(
                    ErrorWrapper(MissingError(), loc=("body", field.alias))
                )
            elif value is not None:
                if isinstance(value, list):
                    values[field.name] = value
                elif isinstance(value, set):
                    values[field.name] = set(value)
                elif isinstance(value, tuple):
                    values[field.name] = tuple(value)
                else:
                    values[field.name] = value
    return values, errors
```

By properly checking if the field alias exists in the received body and handling lists, sets, and tuples correctly, the corrected function should now be able to parse and validate the sequences passed in FormData as expected. This should resolve the validation errors observed in the failing tests.