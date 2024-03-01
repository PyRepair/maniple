## Bug Explanation
The bug in the `request_body_to_args` function arises from the incorrect handling of sequence shapes like `list`, `set`, and `tuple` in the `received_body`. The function is designed to extract values from `received_body` based on the expected `field.alias`, but the way it handles sequences causes the extraction to malfunction. In the failing cases, the function incorrectly treats the entire sequence as a single value, leading to validation errors.

## Bug Fix Strategy
To fix the bug, the function should properly handle sequences in `received_body`. It needs to check if the field type is a sequence and appropriately iterate over the elements to fetch individual values. For sequences like `list`, `set`, and `tuple`, the function should extract values using the `getlist` method of `FormData` and handle them accordingly.

## The Corrected Version of the Function
```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value = None
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                if field.shape == 1:
                    value = received_body.getlist(field.alias)
                elif field.shape == 2:
                    value = set(received_body.getlist(field.alias))
                elif field.shape == 3:
                    value = tuple(received_body.getlist(field.alias))
            else:
                value = received_body.get(field.alias)
        if value is None or (isinstance(field_info, params.Form) and value == ""):
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias))
            else:
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

In the corrected function, we handle different sequence shapes (`list`, `set`, `tuple`) properly by using `getlist` and creating sets or tuples when needed. This modification ensures that each element of the sequence in `received_body` is processed correctly, resolving the original bug and enabling the function to handle sequence-shaped fields as expected.