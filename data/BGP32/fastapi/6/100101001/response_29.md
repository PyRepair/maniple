### Bug Explanation:
The buggy function `request_body_to_args` is designed to convert received request body data into arguments based on the required parameters. However, the bug arises when handling non-typing sequences like lists, sets, and tuples. The current implementation does not correctly handle these cases, resulting in the validation failing and errors being generated.

1. In Case 1 (list parameter as form): the function fails to properly process a list parameter within a form. It generates `MissingError` due to incorrect processing of the list data.
2. In Case 2 (set parameter as form): the function fails similarly to the list case for set parameters.
3. In Case 3 (tuple parameter as form): the function fails to handle tuple data, resulting in `TupleError` being generated.

### Bug Fix Strategy:
To fix the bug in the `request_body_to_args` function, we need to adjust the handling of non-typing sequences (lists, sets, tuples) within form data to correctly extract and process the values. This involves updating the logic to handle sequence shapes appropriately and ensure that the values are correctly populated.

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
                if isinstance(received_body, FormData):
                    if field.alias in received_body:
                        if field.shape in sequence_shapes:
                            value = received_body.getlist(field.alias)
                        else:
                            value = received_body.get(field.alias)

            if (
                value is None
                or (isinstance(field_info, params.Form) and value == "")
                or (
                    isinstance(field_info, params.Form)
                    and field.shape in sequence_shapes
                    and len(value) == 0
                )
            ):
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

            if (
                field.shape in sequence_shapes
                and isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
            ):
                if isinstance(value, UploadFile):
                    value = await value.read()
                else:
                    awaitables = [sub_value.read() for sub_value in value]
                    contents = await asyncio.gather(*awaitables)
                    value = sequence_shape_to_type[field.shape](contents)

            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors
```

With this corrected version, the function should now handle non-typing sequences correctly and pass the failing tests provided.