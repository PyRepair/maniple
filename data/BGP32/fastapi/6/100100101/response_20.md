### Bug Explanation:
The buggy function `request_body_to_args` has an issue with handling sequence types such as lists, sets, and tuples. When processing the input `received_body`, it incorrectly constructs the values according to the passed `field` information, leading to unexpected behavior and errors.

In the failing test cases, the expected input data is in the form of a list, set, or tuple, but the function fails to correctly parse and assign these values based on the type information provided.

### Bug Fix Strategy:
1. Identify the correct way to handle sequence types like lists, sets, and tuples when extracting values from a FormData object.
2. Differentiate the handling of different sequence types correctly to ensure that the values are assigned in the expected format.
3. Pay attention to the field's type information and shape to determine the correct value assignment strategy.

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
                if field.shape in sequence_shapes:  # Check if the field shape is a sequence
                    if isinstance(received_body, FormData):
                        if field.type_ in (list, set, tuple):  # Handle different sequence types
                            value = received_body.getlist(field.alias)
                            if field.type_ is set:
                                value = set(value)
                            elif field.type_ is tuple:
                                value = tuple(value)
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
                and isinstance(value, UploadFile)
            ):
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

With this corrected version, the function should be able to correctly handle values from FormData objects and map them according to the type information provided by the `required_params`. This should address the issues seen in the failing test cases.