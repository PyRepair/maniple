from LLMRepair.utils import (
    find_patch_from_response,
    extract_function_and_imports_from_code_block
)


def test_should_be_able_to_extract_async_function_code():
    test_md_content = """The issue with the `request_body_to_args` function seems to stem from its inability to handle repeated keys in form data, resulting in only the last key-value pair being considered. This causes issues with parsing Python lists, sets, and tuples in the form data, leading to a 422 status code instead of the expected 200.

To fix this issue, the `request_body_to_args` function needs to be updated to properly handle repeated keys in form data. By collecting repeated keys and assigning their values to a list before validation, the function can ensure that all values are accounted for.

Here's the corrected version of the `request_body_to_args` function that addresses this issue:

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
                    values[field.name] = received_body.getlist(field.alias)
                else:
                    values[field.name] = received_body.get(field.alias)
            if values[field.name] is None and field.required:
                errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
            else:
                v_, errors_ = field.validate(values[field.name], values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
    return values, errors
```

With this update, the function should properly handle repeated keys in the form data and parse Python lists, sets, and tuples accordingly.

This fix should resolve the issues raised in the failing tests and the GitHub issue related to supporting repeated key-value pairs in form data."""

    code_fragment = find_patch_from_response(test_md_content, 'request_body_to_args')
    assert len(code_fragment) > 0

    function, imports = extract_function_and_imports_from_code_block(code_fragment, 'request_body_to_args')
    assert len(function) > 0
    assert len(imports) == 0
