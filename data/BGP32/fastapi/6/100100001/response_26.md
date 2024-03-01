## Analysis:
The `request_body_to_args` function is responsible for converting the received body parameters to the appropriate arguments based on the required params. The issue seems to stem from the handling of non-typing sequence shapes like lists, sets, and tuples.

## Potential Error Locations:
1. Conditional check for `sequence_shapes` where the function tries to handle lists fails for Python sets and tuples.
2. Processing logic for non-typing sequence shapes might lead to incorrect outputs.

## Bug Cause:
The bug is likely caused by the fact that the original function does not handle non-typing sequence shapes (like sets and tuples) correctly while converting them from the received body to the appropriate arguments.

## Fix Strategy:
To fix the bug, we need to update the function to correctly handle non-typing sequence shapes like sets and tuples. This involves modifying the conditional checks, value retrieval logic, and processing steps to properly convert the values from the received body.

## Corrected Version:
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
                if field.shape in sequence_shapes:
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)

            if value is None or (isinstance(field_info, params.Form) and value == ""):
                if field.required:
                    errors.append(
                        ErrorWrapper(MissingError(), loc=("body", field.alias))
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
            elif (
                field.shape in sequence_shapes
                and isinstance(value, sequence_types)  # Updated condition here
            ):
                if field.shape == Sequence:
                    value = list(value)  # Convert to list if set or tuple
                elif field.shape == Set:
                    value = set(value)  # Convert to set if list or tuple
                elif field.shape == Tuple:
                    value = tuple(value)  # Convert to tuple if list or set

            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_

    return values, errors
```

By making these changes, the function should now correctly handle non-typing sequence shapes like sets and tuples when converting values from the received body to arguments. This corrected version is expected to pass the failing test cases.