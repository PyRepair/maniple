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

# The source code of the buggy function
```python
# The relative path of the buggy file: fastapi/dependencies/utils.py

# this is the buggy function you need to fix
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

```# A failing test function for the buggy function
```python
# The relative path of the failing test file: tests/test_forms_from_non_typing_sequences.py

def test_python_list_param_as_form():
    response = client.post(
        "/form/python-list", data={"items": ["first", "second", "third"]}
    )
    assert response.status_code == 200
    assert response.json() == ["first", "second", "third"]
```


# A failing test function for the buggy function
```python
# The relative path of the failing test file: tests/test_forms_from_non_typing_sequences.py

def test_python_set_param_as_form():
    response = client.post(
        "/form/python-set", data={"items": ["first", "second", "third"]}
    )
    assert response.status_code == 200
    assert set(response.json()) == {"first", "second", "third"}
```


# A failing test function for the buggy function
```python
# The relative path of the failing test file: tests/test_forms_from_non_typing_sequences.py

def test_python_tuple_param_as_form():
    response = client.post(
        "/form/python-tuple", data={"items": ["first", "second", "third"]}
    )
    assert response.status_code == 200
    assert response.json() == ["first", "second", "third"]
```


Here is a summary of the test cases and error messages:

From the error messages, it can be deduced that each failing test experiences an assertion error. Specifically, each of the failing tests are expecting a "response.status_code" of 200 from the client post but are instead receiving 422 as the response status code according to the error messages in the command line, denoted by "E assert 422 == 200". This means that the actual status code returned by the call is 422, while the assertion is expecting 200.

To simplify the original error message, the failing tests are encountering assertion errors that are comparing the actual response status code of 422 with the expected response status code of 200.

In summary, the tests are failing due to the unexpected status code returned by the client post responses, and not due to a fault in the test code, since the error is regarding a discrepancy in the response status codes.


# Runtime value and type of variables inside the buggy function
Each case below includes input parameter value and type, and the value and type of relevant variables at the function's return, derived from executing failing tests. If an input parameter is not reflected in the output, it is assumed to remain unchanged. Note that some of these values at the function's return might be incorrect. Analyze these cases to identify why the tests are failing to effectively fix the bug.

## Case 1
### Runtime value and type of the input parameters of the buggy function
required_params, value: `[ModelField(name='items', type=list, required=True)]`, type: `list`

received_body, value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: `FormData`

### Runtime value and type of variables right before the buggy function's return
values, value: `{'items': ['first', 'second', 'third']}`, type: `dict`

errors, value: `[]`, type: `list`

field, value: `ModelField(name='items', type=list, required=True)`, type: `ModelField`

field_info, value: `Form(default=Ellipsis, extra={})`, type: `Form`

embed, value: `True`, type: `bool`

field.alias, value: `'items'`, type: `str`

value, value: `['first', 'second', 'third']`, type: `list`

field.shape, value: `1`, type: `int`

field.required, value: `True`, type: `bool`

field.name, value: `'items'`, type: `str`

v_, value: `['first', 'second', 'third']`, type: `list`

## Case 2
### Runtime value and type of the input parameters of the buggy function
required_params, value: `[ModelField(name='items', type=set, required=True)]`, type: `list`

received_body, value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: `FormData`

### Runtime value and type of variables right before the buggy function's return
values, value: `{'items': {'first', 'second', 'third'}}`, type: `dict`

errors, value: `[]`, type: `list`

field, value: `ModelField(name='items', type=set, required=True)`, type: `ModelField`

field_info, value: `Form(default=Ellipsis, extra={})`, type: `Form`

embed, value: `True`, type: `bool`

field.alias, value: `'items'`, type: `str`

value, value: `['first', 'second', 'third']`, type: `list`

field.shape, value: `1`, type: `int`

field.required, value: `True`, type: `bool`

field.name, value: `'items'`, type: `str`

v_, value: `{'first', 'second', 'third'}`, type: `set`

## Case 3
### Runtime value and type of the input parameters of the buggy function
required_params, value: `[ModelField(name='items', type=tuple, required=True)]`, type: `list`

received_body, value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: `FormData`

### Runtime value and type of variables right before the buggy function's return
values, value: `{'items': ('first', 'second', 'third')}`, type: `dict`

errors, value: `[]`, type: `list`

field, value: `ModelField(name='items', type=tuple, required=True)`, type: `ModelField`

field_info, value: `Form(default=Ellipsis, extra={})`, type: `Form`

embed, value: `True`, type: `bool`

field.alias, value: `'items'`, type: `str`

value, value: `['first', 'second', 'third']`, type: `list`

field.shape, value: `1`, type: `int`

field.required, value: `True`, type: `bool`

field.name, value: `'items'`, type: `str`

v_, value: `('first', 'second', 'third')`, type: `tuple`

## Summary of Expected Parameters and Return Values in the Buggy Function

Case 1:
Input:
- required_params: `[ModelField(name='items', type=list, required=True)]`
- received_body: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`

Expected Output:
- values: `{}`
- errors: `[ErrorWrapper(exc=ListError(), loc=('body', 'items'))]`
- field: `ModelField(name='items', type=list, required=True)`
- field_info: `Form(default=Ellipsis, extra={})`
- embed: `True`
- field.alias: `'items'`
- value: `'third'`
- field.shape: `1`
- field.required: `True`
- field.name: `'items'`
- v_: `'third'`
- errors_: `ErrorWrapper(exc=ListError(), loc=('body', 'items'))`

Case 2:
Input:
- required_params: `[ModelField(name='items', type=set, required=True)]`
- received_body: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')]`

Expected Output:
- values: `{}`
- errors: `[ErrorWrapper(exc=SetError(), loc=('body', 'items'))]`
- field: `ModelField(name='items', type=set, required=True)`
- field_info: `Form(default=Ellipsis, extra={})`
- embed: `True`
- field.alias: `'items'`
- value: `'third'`
- field.shape: `1`
- field.required: `True`
- field.name: `'items'`
- v_: `'third'`
- errors_: `ErrorWrapper(exc=SetError(), loc=('body', 'items'))`

Case 3:
Input:
- required_params: `[ModelField(name='items', type=tuple, required=True)]`
- received_body: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')]`

Expected Output:
- values: `{}`
- errors: `[ErrorWrapper(exc=TupleError(), loc=('body', 'items'))]`
- field: `ModelField(name='items', type=tuple, required=True)`
- field_info: `Form(default=Ellipsis, extra={})`
- embed: `True`
- field.alias: `'items'`
- value: `'third'`
- field.shape: `1`
- field.required: `True`
- field.name: `'items'`
- v_: `'third'`
- errors_: `ErrorWrapper(exc=TupleError(), loc=('body', 'items'))`


# A GitHub issue title for this bug
```text
Support repeated key=value in form data
```

## The GitHub issue's detailed description
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

1. Analyze the buggy function and it's relationship with the test code, corresponding error message, the actual input/output variable information, the expected input/output variable information, the github issue.
2. Identify the potential error location within the problematic function.
3. Elucidate the bug's cause using:
   (a). The buggy function
   (b). The failing test
   (c). The corresponding error message
   (d). Discrepancies between actual input/output variable value
   (e). Discrepancies between expected input/output variable value
   (f). The GitHub Issue information

4. Suggest possible approaches for fixing the bug.
5. Present the corrected code for the problematic function such that it satisfied the following:
   (a). Passes the failing test
   (b). Satisfies the expected input/output variable information provided
   (c). Successfully resolves the issue posted in GitHub

