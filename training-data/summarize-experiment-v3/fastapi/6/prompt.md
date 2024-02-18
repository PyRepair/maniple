Please fix the buggy function provided below and output a corrected version.


Your output should follow these steps:
1. Analyze the buggy function and its relationship with the test code, corresponding error message, the actual input/output variable information, the expected input/output variable information, the github issue.
2. Identify a potential error location within the buggy function.
3. Elucidate the bug's cause using:
   (a) The buggy function, 
   (b) The failing test, 
   (c) The corresponding error message, 
   (d) The actual input/output variable values, 
   (e) The expected input/output variable values, 
   (f) The GitHub Issue information

4. Suggest approaches for fixing the bug.
5. Present the corrected code for the buggy function such that it satisfied the following:
   (a) the program passes the failing test, 
   (b) the function satisfies the expected input/output variable information provided, 
   (c) successfully resolves the issue posted in GitHub




## The source code of the buggy function

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

The buggy function is under file: `/home/ubuntu/Desktop/bgp_envs_local/repos/fastapi_6/fastapi/dependencies/utils.py`

Here is the buggy function:
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


## Summary of the test cases and error messages

The failing tests of the `test_python_list_param_as_form()`, `test_python_set_param_as_form()`, and `test_python_tuple_param_as_form()` return the same error message, stating that the assertion of the status code to be equal to 200 fails due to a difference of 422 and 200. The relevant stack frame of the `request_body_to_args` function is suspected to lie in the logic responsible for parsing the request body and validating the incoming data. Therefore, the fault in the buggy function is likely linked to the parsing and validation of sequence input types such as lists, sets, and tuples.


## Summary of Runtime Variables and Types in the Buggy Function

The relevant input/output values are:

## Case 1
- Input parameters: required_params (value: `[ModelField(name='items', type=list, required=True)]`, type: list), received_body (value: FormData([('items', 'first'), ('items', 'second'), ('items', 'third')]), type: FormData)
- Output: values (value: {'items': ['first', 'second', 'third']}, type: dict)
Rational: The function is expected to convert the received body into a list for the 'items' key, but it incorrectly converts it into a dict.

## Case 2
- Input parameters: required_params (value: `[ModelField(name='items', type=set, required=True)]`, type: list), received_body (value: FormData([('items', 'first'), ('items', 'second'), ('items', 'third')]), type: FormData)
- Output: values (value: {'items': {'first', 'second', 'third'}}, type: dict)
Rational: The function is expected to convert the received body into a set for the 'items' key, but it incorrectly converts it into a dict.

## Case 3
- Input parameters: required_params (value: `[ModelField(name='items', type=tuple, required=True)]`, type: list), received_body (value: FormData([('items', 'first'), ('items', 'second'), ('items', 'third')]), type: FormData)
- Output: values (value: {'items': ('first', 'second', 'third')}, type: dict)
Rational: The function is expected to convert the received body into a tuple for the 'items' key, but it incorrectly converts it into a dict.


## Summary of Expected Parameters and Return Values in the Buggy Function

In all the expected cases, the function is expected to populate the 'values' and 'errors' variables based on the received parameters and body. However, in all cases, the 'values' variable is expected to be an empty dictionary, but the current implementation does not seem to fulfill this expectation. Additionally, the expected list of errors and the errors generated by the function do not match in any of the cases, indicating a discrepancy between the current and expected outputs. These differences suggest that the function is not working as intended and may contain a bug.


# A GitHub issue for this bug

The issue's title:
```text
Support repeated key=value in form data
```

The issue's detailed description:
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

