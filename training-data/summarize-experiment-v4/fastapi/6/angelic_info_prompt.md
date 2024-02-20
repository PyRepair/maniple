Your task is to summarize the expected input and output values of a buggy function, following the example provided below.

## Example source code of the buggy function
```python
def calculate_total_cost(nights, rate_per_night):
    discount = 0.1  # 10% discount for stays longer than 7 nights
    if nights > 7:
        total_cost = nights * rate_per_night * (1 - discount)
    else:
        total_cost = nights * rate_per_night
    return total_cost
```

## Example expected value and type of variables during the failing test execution

### Expected case 1
#### Input parameter value and type
nights, value: `8`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `790`, type: `int`

### Expected case 2
#### Input parameter value and type
nights, value: `9`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `880`, type: `int`

### Expected Case 3
#### Input parameter value and type
nights, value: `7`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `700`, type: `int`

### Exptected Case 4
#### Input parameter value and type
nights, value: `10`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `970`, type: `int`


## Example summary:
Case 1: Given the input parameters `nights=8` and `rate_per_night=100`, the function should return `790`. This might be calculated by `7 * 100 + 100 * 0.9 = 790`.

Case2: Given the input parameters `nights=9` and `rate_per_night=100`, the function should return `880`. This might be calculated by `7 * 100 + 2 * 100 * 0.9 = 880`.

Case3: Given the input parameters `nights=7` and `rate_per_night=100`, the function should return `700`. This might be calculated by `7 * 100 = 700`.

Case4: Given the input parameters `nights=10` and `rate_per_night=100`, the function should return `970`. This might be calculated by `7 * 100 + 3 * 100 * 0.9 = 970`.



## The source code of the buggy function

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

## Expected values and types of variables during the failing test execution
Each case below includes input parameter values and types, and the expected values and types of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.

### Expected case 1
#### The values and types of buggy function's parameters
required_params, value: `[ModelField(name='items', type=list, required=True)]`, type: `list`

received_body, value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: `FormData`

#### Expected values and types of variables right before the buggy function's return
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

### Expected case 2
#### The values and types of buggy function's parameters
required_params, value: `[ModelField(name='items', type=set, required=True)]`, type: `list`

received_body, value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: `FormData`

#### Expected values and types of variables right before the buggy function's return
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

### Expected case 3
#### The values and types of buggy function's parameters
required_params, value: `[ModelField(name='items', type=tuple, required=True)]`, type: `list`

received_body, value: `FormData([('items', 'first'), ('items', 'second'), ('items', 'third')])`, type: `FormData`

#### Expected values and types of variables right before the buggy function's return
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

## Summary:

[Your summary here.]