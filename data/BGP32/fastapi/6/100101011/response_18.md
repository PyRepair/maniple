### Bug Explanation:
The bug in the `request_body_to_args` function arises from the handling of non-typing sequences in the request body. Specifically, when dealing with non-typing sequences like lists, sets, or tuples in the form data, the function fails to correctly interpret the nested values, leading to errors in validation and missing data handling.

In the provided cases:
1. The function fails to properly process the input where a python list is passed as form data. It incorrectly generates an error due to an issue with processing the list in the form data.
2. Similar behavior is witnessed in the case of passing a python set as form data where the function wrongly handles the sequence, resulting in an error.
3. The same issue occurs when passing a python tuple as form data, causing the function to misinterpret the data structure.

### Bug Fix Strategy:
1. Update the function to correctly parse non-typing sequences passed in form data to ensure proper validation and handling of the sequences as expected.
2. Modify the logic to handle repeated keys and values in form data, converting them into lists as per the GitHub issue's suggestion to support repeated key-value pairs in form data.

### Corrected Function:
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
                if field.alias in received_body:
                    value = received_body.getlist(field.alias)
            if value is None:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
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

The corrected version of the function now accurately processes non-typing sequences in the form data and handles repeated keys appropriately to meet the expectations outlined in the GitHub issue.