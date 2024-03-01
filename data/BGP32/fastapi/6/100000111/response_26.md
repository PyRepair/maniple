## Bug Explanation

The bug in the `request_body_to_args` function arises from the incorrect handling of repeated key-value pairs in the `FormData` when processing them into arguments. The issue described in the GitHub problem relates to this bug as the existing implementation only captures the last value of a repeated key in the `FormData`.

The code assumes a single value for each key, but in the case of repeated keys like `items`, the function should generate a list, set, or tuple containing all values associated with that key. The issue on GitHub suggests that FastAPI should collect all values for a repeated key and process them accordingly.

## Bug Fix Strategy

To fix the bug, the function needs to properly handle repeated keys in the `FormData`. Instead of overwriting existing values, the code should accumulate all values associated with a key if it appears multiple times. Furthermore, the function should correctly process the values based on the type of the field (list, set, tuple) and perform the necessary validations.

## Corrected Function

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
                        if field.shape == FormDataShape.LIST:
                            value = received_body.getlist(field.alias)
                        elif field.shape == FormDataShape.SET:
                            value = set(received_body.getlist(field.alias))
                        elif field.shape == FormDataShape.TUPLE:
                            value = tuple(received_body.getlist(field.alias))
                    else:
                        value = field.default

            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_

    return values, errors
```

In the corrected version:
- The function iterates over all fields in `required_params` to process each field individually.
- It checks if the field alias is present in the `received_body` `FormData`.
- If the field alias is present:
  - For list-shaped fields, it retrieves multiple values using `getlist`.
  - For set-shaped fields, it converts the list of values to a set.
  - For tuple-shaped fields, it converts the list of values to a tuple.
- If the field alias is not present, it assigns the default value of the field.
- It then validates and stores the processed value and handles potential errors correctly.