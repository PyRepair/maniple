## Bug Explanation
The buggy function `request_body_to_args` is not correctly handling the case when the required parameter is a sequence type (such as list, set, tuple) in the request body. It fails to properly extract the values from the `received_body` based on the parameter's type and alias.

In Case 1, the `received_body` contains multiple values for the 'items' key, but the function incorrectly assigns only the last value to the 'items' field, resulting in missing values in the final output.

In Cases 2 and 3, similar issues occur, where the function does not correctly handle sequence types like set and tuple.

## Bug Fix Strategy
To fix the bug in the `request_body_to_args` function, we need to iterate through each field in `required_params` and handle the extraction of values based on the field's type. For sequence types, we should ensure that all values corresponding to the field's alias are extracted.

The function needs to be modified to handle various sequence shapes properly and store the values accordingly in the `values` dictionary.

## Corrected Version of the Function
Here is the corrected version of the `request_body_to_args` function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        if received_body:
            value = None
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
                values[field.name] = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
                if value is None:
                    value = received_body.getlist(field.alias)
                if len(value) == 1:
                    value = value[0]
                values[field.name] = value
        else:
            if field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                values[field.name] = deepcopy(field.default)
    return values, errors
```

This corrected version should now handle all cases correctly and extract values for sequence types like list, set, and tuple appropriately from the `received_body`.