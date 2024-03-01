### Analysis:
1. The function `request_body_to_args` takes a list of required ModelField parameters and received body data to extract values based on the parameters.
2. The function checks each parameter to extract the corresponding value from the received body.
3. Errors are accumulated in case of missing data for required fields.

### Issues:
1. In the failing tests, the response status code is expected to be 200 but is actually returning a 422 status code, indicating a validation error.
2. The function doesn't handle sequence types like lists, sets, and tuples appropriately, leading to validation failures.

### Bug Cause:
1. The function does not handle sequence shapes correctly for FormData inputs, leading to incorrect value extraction for list, set, and tuple types.
2. This causes validation issues and results in a 422 response status instead of 200.

### Solution:
1. Update the function to correctly handle sequence shapes in the received body.
2. Ensure that values extracted for different sequence types are properly validated and processed.

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
            value = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(received_body, FormData):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            if (
                value is None
                or (isinstance(get_field_info(field), params.Form) and value == "")
                or (
                    isinstance(get_field_info(field), params.Form)
                    and field.shape in sequence_shapes
                    and len(value) == 0
                )
            ):
                if field.required:
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
                isinstance(get_field_info(field), params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif (
                field.shape in sequence_shapes
                and isinstance(get_field_info(field), params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, sequence_types)
            ):
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

With this corrected function, the values extracted from the body for sequence types like lists, sets, and tuples will be handled appropriately, resolving the validation issues and ensuring the expected 200 response status in the failing tests.