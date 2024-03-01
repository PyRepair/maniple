### Bug Explanation

The buggy function `request_body_to_args` is not handling sequences correctly when receiving data in a FormData format. The function is designed to extract values from a request body based on required parameters, but it fails to handle sequences like lists, sets, and tuples appropriately. This leads to errors being generated for each element in the sequence instead of processing the sequence itself as a whole.

In the provided examples, the function is parsing `FormData` where the values for the "items" key are a list of strings. However, the function treats each value as a separate entity, resulting in errors being created for each item rather than handling the entire sequence as a single entity.

### Bug Fix Strategy

To fix the bug, we need to adjust how the function processes sequences like lists, sets, and tuples when receiving data in a FormData format. We should ensure that the function correctly handles these sequence types as a whole rather than treating individual elements separately. This involves modifying the conditional checks and extraction logic for sequence shapes in the function.

### Corrected Version of the Function

```python
async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        field = required_params[0]
        field_info = get_field_info(field)
        embed = getattr(field_info, "embed", None)
        if len(required_params) == 1 and not embed:
            received_body = {field.alias: received_body}
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if (
                    field.shape in sequence_shapes
                    and isinstance(received_body, FormData)
                    and received_body.getlist(field.alias)
                ):
                    values[field.name] = received_body.getlist(field.alias)
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
                            ErrorWrapper(  # type: ignore
                                MissingError(),
                                loc=("body", field.alias),
                                config=BaseConfig,
                            )
                        )
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            if isinstance(field_info, params.File) and lenient_issubclass(field.type_, bytes):
                if not isinstance(value, sequence_types):
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

The corrected version of the function adjusts the handling of sequence shapes in the `request_body_to_args` function. Now, sequences like lists, sets, and tuples are processed correctly as a whole when receiving data from a FormData format. This fix should address the issues seen in the failing tests.