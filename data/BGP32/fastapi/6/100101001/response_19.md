### Bug Explanation:

The bug in the `request_body_to_args` function arises from how it handles different types of sequences (`list`, `set`, `tuple`) when received as form data. The function fails to correctly extract and validate the values from the form data for sequences other than lists, leading to validation errors and incorrect outputs.

In the runtime values provided:
- For Case 1 (List): The function incorrectly handles the list values and generates an error for the sequence shape of `1`.
- For Case 2 (Set): It fails to handle sets properly and generates a `SetError`.
- For Case 3 (Tuple): Similar issues occur for tuples resulting in a `TupleError`.

The function does not correctly process the data for sets and tuples, causing validation errors and failures in the tests.

### Fix Strategy:

To address the bug in the `request_body_to_args` function, the handling of different sequence shapes (lists, sets, tuples) needs to be improved. Specifically, the function should correctly handle values for sets and tuples similar to how it handles lists.

One approach to fixing this bug is to refactor the logic for extracting values from the form data based on the shape of the fields (list, set, tuple). Additionally, ensuring that the validation process accounts for the correct sequence shapes and handles them appropriately will help in resolving the issues.

### Corrected Version of the Function:

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
                    if field.shape == 0:
                        value = [received_body.get(field.alias, [])]
                    elif field.shape == 1:
                        value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
                    
            if (value is None
                or (isinstance(field_info, params.Form) and value == "")
                or (isinstance(field_info, params.Form)
                    and field.shape in sequence_shapes and len(value) == 0)):
                
                if field.required:
                    if PYDANTIC_1:
                        errors.append(
                            ErrorWrapper(MissingError(), loc=("body", field.alias))
                        )
                    else:
                        errors.append(
                            ErrorWrapper(
                                MissingError(),
                                loc=("body", field.alias),
                                config=BaseConfig,
                            )
                        )
                else:
                    values[field.name] = deepcopy(field.default)
                continue
                
            if (isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)):
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

By modifying how the function handles different types of sequences (`list`, `set`, `tuple`) and their corresponding values in the form data, the corrected version should pass the failing tests provided.