The bug in the `request_body_to_args` function lies in the incorrect handling of sequence-shaped fields (lists, sets, tuples) in the received body. The function fails to properly extract values from `FormData` for sequence-shaped fields, leading to validation errors.

To fix the bug, we need to adjust how values are retrieved for sequence-shaped fields and ensure they are validated correctly. Here is the corrected version of the function:

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value: Any = None
        if received_body is not None:
            if field.shape in sequence_shapes and isinstance(
                received_body, FormData
            ):
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
                else:  # pragma: nocover
                    errors.append(
                        ErrorWrapper(  # type: ignore
                            MissingError(),
                            loc=("body", field.alias),
                            config=BaseConfig,
                        )
                    )
            else:
                values[field.name] = deepcopy(field.default)
            continue
        if (
            isinstance(field_info, params.File)
            and lenient_issubclass(field.type_, bytes)
            and isinstance(value, list)
        ):
            if field.shape == 1:  # List
                value = await asyncio.gather(*[v.read() for v in value])
            else:  # Set or Tuple
                awaitables = [v.read() for v in value]
                results = await asyncio.gather(*awaitables)
                
                if field.shape == 2:  # Set
                    value = set(results)
                else:  # Tuple
                    value = tuple(results)
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
1. We iterate through each required parameter field and properly handle sequence-shaped fields by checking if the received body is a `FormData`.
2. For sequence-shaped fields and file types, we adjust the value extraction logic to handle lists, sets, and tuples appropriately.
3. We validate the extracted values and handle errors as before.

By applying these modifications, the function should now handle sequence-shaped fields correctly and validate the received data properly.