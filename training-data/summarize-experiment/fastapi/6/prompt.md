Please correct the malfunctioning function provided below by using the relevant information listed to address this bug. Then, produce a revised version of the function that resolves the issue. When outputting the fix, output the entire function so that the output can be used as a drop-in replacement for the buggy version of the function.

Assume that the following list of imports are available in the current environment, so you don't need to import them when generating a fix.
```python
import asyncio
from copy import deepcopy
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple, Type, Union, cast
from fastapi import params
from fastapi.utils import PYDANTIC_1, get_field_info, get_path_param_names
from pydantic import BaseConfig, BaseModel, create_model
from pydantic.error_wrappers import ErrorWrapper
from pydantic.errors import MissingError
from pydantic.utils import lenient_issubclass
from starlette.datastructures import FormData, Headers, QueryParams, UploadFile
from pydantic.fields import Field as ModelField
```

The following is the buggy function that you need to fix:
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
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif (
                field.shape in sequence_shapes
                and isinstance(field_info, params.File)
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



The followings are test functions under directory `tests/test_forms_from_non_typing_sequences.py` in the project.
```python
def test_python_list_param_as_form():
    response = client.post(
        "/form/python-list", data={"items": ["first", "second", "third"]}
    )
    assert response.status_code == 200
    assert response.json() == ["first", "second", "third"]

def test_python_set_param_as_form():
    response = client.post(
        "/form/python-set", data={"items": ["first", "second", "third"]}
    )
    assert response.status_code == 200
    assert set(response.json()) == {"first", "second", "third"}

def test_python_tuple_param_as_form():
    response = client.post(
        "/form/python-tuple", data={"items": ["first", "second", "third"]}
    )
    assert response.status_code == 200
    assert response.json() == ["first", "second", "third"]
```

The error message that corresponds the the above test functions is:
```
def test_python_tuple_param_as_form():
        response = client.post(
            "/form/python-tuple", data={"items": ["first", "second", "third"]}
        )
>       assert response.status_code == 200
E       assert 422 == 200
E         +422
E         -200

tests/test_forms_from_non_typing_sequences.py:45: AssertionError
```



## Summary of Runtime Variables and Types in the Buggy Function

In this buggy function, `request_body_to_args`, variables `required_params` and `received_body` are used as input parameters. Additionally, variables `values` and `errors` are initialized as an empty dictionary and an empty list, respectively.

In the first test case, `required_params` is a list containing one element of type `ModelField` with the name 'items', type 'list', and it's required. `received_body` is of type `FormData` with the values ('items', 'first'), ('items', 'second'), and ('items', 'third'). When the buggy function returns, the `values` dictionary is populated with the `'items'` key containing a list `['first', 'second', 'third']`, and `errors` remains an empty list.

In the second test case, we observe the same `required_params` and `received_body` values as in case 1. When the buggy function returns, the `values` dictionary is populated with the `'items'` key containing a set `{'third', 'second', 'first'}`, and `errors` remains an empty list.

In the third test case, `required_params` is a list containing one element of type `ModelField` with the name 'items', type 'tuple', and it's required. `received_body` is of type `FormData` with the values ('items', 'first'), ('items', 'second'), and ('items', 'third'). When the buggy function returns, the `values` dictionary is populated with the `'items'` key containing a tuple `('first', 'second', 'third')`, and `errors` remains an empty list.

Upon analyzing the buggy function and the variables associated with it, it seems that the issue arises from the logic used to process the `received_body` and populate the `values` and `errors`. Further debugging and code exploration are necessary to identify and fix the bug.



## Summary of Expected Parameters and Return Values in the Buggy Function

In the given function, the core logic involves checking for missing or incorrect inputs based on the received body and required parameters, and then validating and building the return values accordingly.

The function begins by initializing `values` as an empty dictionary and `errors` as an empty list. It then proceeds to handle missing or incorrect inputs by iterating over the `required_params`. It checks if the `received_body` is None and extracts values using the `field.alias`. If no value is found and the field is required, an error is appended to the `errors` list, and the default value for the field is added to the `values` dictionary. If a value is found, it is validated using the `field.validate` method, and the results are appended to the `errors` list or added to the `values` dictionary accordingly.

The function uses different cases for sequence and file-shaped fields while also accounting for specific types such as set, list, and tuple. If a file-shaped field type is found, it checks for the correct type and processes the value accordingly.

Overall, the function's core logic centers around iterating through required parameters, checking for missing or incorrect inputs, and building the `values` and `errors` based on the input parameters and received body.

It appears that the function is handling different cases based on the type and shape of the input parameters, checking for required, missing, or incorrect inputs, and validating the values before constructing the final `values` and `errors` outputs. The errors are also being handled based on field shape and required status, appending the appropriate error message to the `errors` list.



# A GitHub issue title for this bug
```text
Support repeated key=value in form data
```

## The associated detailed issue description
```text
Is your feature request related to a problem
Yes.

Given some URL encoded data like this...

choices=parrot&choices=spider
...only the last key=value wins.

This does not work like I expected:

choices: list = Form(...)
You can only validate against the last value.

The solution you would like
Perhaps FastAPI should collect repeated keys in the 2-tuple list that request.form() gives and assign those values as a list to the same key before validation happens.
```





# Instructions

1. Analyze the test case and its relationship with the error message, if applicable.
2. Identify the potential error location within the problematic function.
3. Explain the reasons behind the occurrence of the bug.
4. Suggest possible approaches for fixing the bug.
5. Present the corrected code for the problematic function.