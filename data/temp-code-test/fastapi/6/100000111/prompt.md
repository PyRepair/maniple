Please fix the buggy function provided below and output a corrected version.
Following these steps:
1. Analyze the buggy function and its relationship with the expected input/output values, the GitHub issue.
2. Identify potential error locations within the buggy function.
3. Explain the cause of the bug using the buggy function, the expected input/output variable values, the GitHub Issue information.
4. Suggest a strategy for fixing the bug.
5. Given the buggy function below, provide a corrected version. The corrected version should satisfy the expected input/output values, resolve the issue posted in GitHub.


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

## The source code of the buggy function
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

```






## Expected values and types of variables during the failing test execution
Each case below includes input parameter values and types, and the expected values and types of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.

### Expected case 1
#### The values and types of buggy function's parameters
required_params, expected value: `[ModelField(name='items', type=list, required=True)]`, type: `list`

received_body, expected value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: `FormData`

#### Expected values and types of variables right before the buggy function's return
values, expected value: `{'items': ['first', 'second', 'third']}`, type: `dict`

errors, expected value: `[]`, type: `list`

field, expected value: `ModelField(name='items', type=list, required=True)`, type: `ModelField`

field_info, expected value: `Form(default=Ellipsis, extra={})`, type: `Form`

embed, expected value: `True`, type: `bool`

field.alias, expected value: `'items'`, type: `str`

value, expected value: `['first', 'second', 'third']`, type: `list`

field.shape, expected value: `1`, type: `int`

field.required, expected value: `True`, type: `bool`

field.name, expected value: `'items'`, type: `str`

v_, expected value: `['first', 'second', 'third']`, type: `list`

### Expected case 2
#### The values and types of buggy function's parameters
required_params, expected value: `[ModelField(name='items', type=set, required=True)]`, type: `list`

received_body, expected value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: `FormData`

#### Expected values and types of variables right before the buggy function's return
values, expected value: `{'items': {'first', 'second', 'third'}}`, type: `dict`

errors, expected value: `[]`, type: `list`

field, expected value: `ModelField(name='items', type=set, required=True)`, type: `ModelField`

field_info, expected value: `Form(default=Ellipsis, extra={})`, type: `Form`

embed, expected value: `True`, type: `bool`

field.alias, expected value: `'items'`, type: `str`

value, expected value: `['first', 'second', 'third']`, type: `list`

field.shape, expected value: `1`, type: `int`

field.required, expected value: `True`, type: `bool`

field.name, expected value: `'items'`, type: `str`

v_, expected value: `{'first', 'second', 'third'}`, type: `set`

### Expected case 3
#### The values and types of buggy function's parameters
required_params, expected value: `[ModelField(name='items', type=tuple, required=True)]`, type: `list`

received_body, expected value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: `FormData`

#### Expected values and types of variables right before the buggy function's return
values, expected value: `{'items': ('first', 'second', 'third')}`, type: `dict`

errors, expected value: `[]`, type: `list`

field, expected value: `ModelField(name='items', type=tuple, required=True)`, type: `ModelField`

field_info, expected value: `Form(default=Ellipsis, extra={})`, type: `Form`

embed, expected value: `True`, type: `bool`

field.alias, expected value: `'items'`, type: `str`

value, expected value: `['first', 'second', 'third']`, type: `list`

field.shape, expected value: `1`, type: `int`

field.required, expected value: `True`, type: `bool`

field.name, expected value: `'items'`, type: `str`

v_, expected value: `('first', 'second', 'third')`, type: `tuple`



## A GitHub issue for this bug

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



