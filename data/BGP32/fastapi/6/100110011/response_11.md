### Bug Analysis:
1. The `request_body_to_args` function is supposed to process the request body and extract values for the required parameters. However, it seems to have issues handling form data with sequence shapes like lists, sets, and tuples.
2. The failing tests are expecting a status code of 200, but the current implementation of `request_body_to_args` is causing validation errors, leading to a status code of 422.
3. The errors are caused when processing sequence shapes in the request body due to incorrect handling of form data values.
4. To fix the bug, we need to correctly process and extract values from form data with sequence shapes and ensure that the required parameters are handled properly.
5. The corrected version of the function should handle sequence shapes in the request body correctly and return the extracted values without validation errors.

### Bug Fix:
Here is the corrected version of the `request_body_to_args` function:

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
            if field.shape in sequence_shapes and isinstance(
                received_body, FormData
            ):
                value = received_body.getlist(field.alias)
            else:
                value = received_body.get(field.alias)
                
        if value is None or value == "":
            if field.required:
                errors.append(
                    ErrorWrapper(MissingError(), loc=("body", field.alias))
                )
            else:
                if field.default is not None:
                    values[field.name] = deepcopy(field.default)
        else:
            if (
                isinstance(field.default, list)
                and field.shape in sequence_shapes
                and not isinstance(value, list)
            ):
                value = [value]
                
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_

    return values, errors
```

By making the above corrections and adjustments in the function, it should now correctly handle form data with sequence shapes like lists, sets, and tuples, and properly extract the values for the required parameters.

This should resolve the validation errors and allow the tests to pass successfully.