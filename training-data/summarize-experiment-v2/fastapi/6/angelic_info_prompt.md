You have been given the source code of a function that is currently failing its test cases. Your task is to create a short version of expected input and output value pair by removing some unnecessary or less important variable. This involves examining how the input parameters relate to the return values, based on the buggy function's source code.


# Expected value and type of variables during the failing test execution
Each case below includes input parameter value and type, and the expected value and type of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.

## Expected case 1
### Input parameter value and type
required_params, value: `[ModelField(name='items', type=list, required=True)]`, type: `list`

received_body, value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: `FormData`

### Expected value and type of variables right before the buggy function's return
values, expected value: `{}`, type: `dict`

errors, expected value: `[ErrorWrapper(exc=ListError(), loc=('body', 'items'))]`, type: `list`

field, expected value: `ModelField(name='items', type=list, required=True)`, type: `ModelField`

field_info, expected value: `Form(default=Ellipsis, extra={})`, type: `Form`

embed, expected value: `True`, type: `bool`

field.alias, expected value: `'items'`, type: `str`

value, expected value: `'third'`, type: `str`

field.shape, expected value: `1`, type: `int`

field.required, expected value: `True`, type: `bool`

field.name, expected value: `'items'`, type: `str`

v_, expected value: `'third'`, type: `str`

errors_, expected value: `ErrorWrapper(exc=ListError(), loc=('body', 'items'))`, type: `ErrorWrapper`

## Expected case 2
### Input parameter value and type
required_params, value: `[ModelField(name='items', type=set, required=True)]`, type: `list`

received_body, value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: `FormData`

### Expected value and type of variables right before the buggy function's return
values, expected value: `{}`, type: `dict`

errors, expected value: `[ErrorWrapper(exc=SetError(), loc=('body', 'items'))]`, type: `list`

field, expected value: `ModelField(name='items', type=set, required=True)`, type: `ModelField`

field_info, expected value: `Form(default=Ellipsis, extra={})`, type: `Form`

embed, expected value: `True`, type: `bool`

field.alias, expected value: `'items'`, type: `str`

value, expected value: `'third'`, type: `str`

field.shape, expected value: `1`, type: `int`

field.required, expected value: `True`, type: `bool`

field.name, expected value: `'items'`, type: `str`

v_, expected value: `'third'`, type: `str`

errors_, expected value: `ErrorWrapper(exc=SetError(), loc=('body', 'items'))`, type: `ErrorWrapper`

## Expected case 3
### Input parameter value and type
required_params, value: `[ModelField(name='items', type=tuple, required=True)]`, type: `list`

received_body, value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: `FormData`

### Expected value and type of variables right before the buggy function's return
values, expected value: `{}`, type: `dict`

errors, expected value: `[ErrorWrapper(exc=TupleError(), loc=('body', 'items'))]`, type: `list`

field, expected value: `ModelField(name='items', type=tuple, required=True)`, type: `ModelField`

field_info, expected value: `Form(default=Ellipsis, extra={})`, type: `Form`

embed, expected value: `True`, type: `bool`

field.alias, expected value: `'items'`, type: `str`

value, expected value: `'third'`, type: `str`

field.shape, expected value: `1`, type: `int`

field.required, expected value: `True`, type: `bool`

field.name, expected value: `'items'`, type: `str`

v_, expected value: `'third'`, type: `str`

errors_, expected value: `ErrorWrapper(exc=TupleError(), loc=('body', 'items'))`, type: `ErrorWrapper`