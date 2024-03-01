### Bug Explanation
The bug in the `request_body_to_args` function is caused by the logic to handle sequence shapes when dealing with non-typing sequences (like lists, sets, and tuples) in the received body for form data. The current implementation does not correctly handle non-typing sequences, resulting in errors when parsing and validating the data.

1. In the first failing test case, the function fails to recognize the list nature of the 'items' field in the form data, leading to an error indicating that a list is expected but a string is provided.
2. In the second failing test case, the function fails to recognize the set nature of the 'items' field in the form data, resulting in an error due to the mismatch between expected set type and string type.
3. In the third failing test case, the function fails to recognize the tuple nature of the 'items' field in the form data, causing an error similar to the first failing test case.

### Bug Fix Strategy
To fix the bug in the `request_body_to_args` function, we need to update the logic that handles non-typing sequences in the received body. Specifically, we should correctly identify the type of the payload field (list, set, tuple) and appropriately parse and validate the data.

### Corrected Version
```python
import asyncio
from copy import deepcopy
from typing import Any, Dict, List, Tuple, Union
from pydantic.fields import Field as ModelField
from starlette.datastructures import FormData
from pydantic.error_wrappers import ErrorWrapper
from pydantic.errors import MissingError
from fastapi.utils import PYDANTIC_1, get_field_info
from fastapi import params

async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    
    if required_params:
        field = required_params[0]
        
        for field in required_params:
            value = None
            
            if received_body is not None:
                value = received_body.getlist(field.alias) if field.shape in [1, 2] else received_body.get(field.alias)
            
            if value is None:
                if field.required:
                    if PYDANTIC_1:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias)))
                    else:
                        errors.append(ErrorWrapper(MissingError(), loc=("body", field.alias), config=BaseConfig))
                else:
                    values[field.name] = deepcopy(field.default)
            else:
                v_, errors_ = field.validate(value, values, loc=("body", field.alias))
                if isinstance(errors_, ErrorWrapper):
                    errors.append(errors_)
                elif isinstance(errors_, list):
                    errors.extend(errors_)
                else:
                    values[field.name] = v_
    
    return values, errors
```

After making these corrections, the `request_body_to_args` function should be able to correctly parse and handle non-typing sequences in the received form data for lists, sets, and tuples, passing the failing test cases.