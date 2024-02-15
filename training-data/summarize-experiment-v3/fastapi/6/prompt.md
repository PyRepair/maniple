Please fix the buggy function provided below and output a corrected version. When outputting the fix, output the entire function so that the output can be used as a drop-in replacement for the buggy version of the function.


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

```


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

The failing tests for functions `test_python_list_param_as_form`, `test_python_set_param_as_form`, and `test_python_tuple_param_as_form` are due to the buggy function `request_body_to_args` in `fastapi/dependencies/utils.py` file. A common error message `assert 422 == 200` confirms that all three tests are failing at the `assert response.status_code == 200` line. It appears that the function is not handling the form data input for the parameters that needs the expected format for list, set, and tuple. The bug might be due to the incorrect handling of form data for these non-typing sequences.


## Summary of Runtime Variables and Types in the Buggy Function

The relevant runtime input/output values are:
- Input parameters: required_params (value: `[ModelField(name='items', type=list, required=True)]`, type: list), received_body (value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: FormData)
- Output: values (value: `{'items': ['first', 'second', 'third']}`, type: dict), errors (value: `[]`, type: list)
Rationale: The function is intended to process different data types but behaves inconsistently, leading to incorrect type assignments and corresponding output values.


## Summary of Expected Parameters and Return Values in the Buggy Function

The buggy function `request_body_to_args` is not returning the expected values and types of variables, based on the provided cases. In each case, there are discrepancies between the expected and the actual outputs of the function. For example, in case 1, the expected value for `values` is an empty dictionary, but the function is returning non-empty values. Similar discrepancies exist in other cases as well. The function should be reviewed to address the issues and reconcile the differences between the expected and actual outputs.


## Summary of the GitHub Issue Related to the Bug

The issue reported relates to FastAPI's inability to properly handle repeated key=value pairs in form data. The `request_body_to_args` function currently does not collect repeated keys in the 2-tuple list that `request.form()` gives, and hence assigns only the last value to the key before validation happens. This behavior is contradictory to the expected functionality, where the repeated keys should be collected and assigned as a list to the same key before validation. The issue seems to stem from the handling of form data and the validation process within the function.


