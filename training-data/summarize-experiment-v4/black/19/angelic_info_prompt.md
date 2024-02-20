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
def _maybe_empty_lines(self, current_line: Line) -> Tuple[int, int]:
    max_allowed = 1
    if current_line.depth == 0:
        max_allowed = 2
    if current_line.leaves:
        # Consume the first leaf's extra newlines.
        first_leaf = current_line.leaves[0]
        before = first_leaf.prefix.count("\n")
        before = min(before, max_allowed)
        first_leaf.prefix = ""
    else:
        before = 0
    depth = current_line.depth
    while self.previous_defs and self.previous_defs[-1] >= depth:
        self.previous_defs.pop()
        before = 1 if depth else 2
    is_decorator = current_line.is_decorator
    if is_decorator or current_line.is_def or current_line.is_class:
        if not is_decorator:
            self.previous_defs.append(depth)
        if self.previous_line is None:
            # Don't insert empty lines before the first line in the file.
            return 0, 0

        if self.previous_line and self.previous_line.is_decorator:
            # Don't insert empty lines between decorators.
            return 0, 0

        newlines = 2
        if current_line.depth:
            newlines -= 1
        return newlines, 0

    if current_line.is_flow_control:
        return before, 1

    if (
        self.previous_line
        and self.previous_line.is_import
        and not current_line.is_import
        and depth == self.previous_line.depth
    ):
        return (before or 1), 0

    if (
        self.previous_line
        and self.previous_line.is_yield
        and (not current_line.is_yield or depth != self.previous_line.depth)
    ):
        return (before or 1), 0

    return before, 0

```

## Expected values and types of variables during the failing test execution
Each case below includes input parameter values and types, and the expected values and types of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.

### Expected case 1
#### The values and types of buggy function's parameters
current_line.depth, value: `0`, type: `int`

current_line, value: `Line(depth=0, leaves=[Leaf(AT, '@'), Leaf(NAME, 'property')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(NAME, 'property'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.leaves, value: `[Leaf(AT, '@'), Leaf(NAME, 'property')]`, type: `list`

self.previous_defs, value: `[]`, type: `list`

self, value: `EmptyLineTracker(previous_line=None, previous_after=0, previous_defs=[])`, type: `EmptyLineTracker`

current_line.is_decorator, value: `True`, type: `bool`

current_line.is_def, value: `False`, type: `bool`

current_line.is_class, value: `False`, type: `bool`

current_line.is_flow_control, value: `False`, type: `bool`

current_line.is_import, value: `False`, type: `bool`

current_line.is_yield, value: `False`, type: `bool`

#### Expected values and types of variables right before the buggy function's return
max_allowed, expected value: `2`, type: `int`

first_leaf, expected value: `Leaf(AT, '@')`, type: `Leaf`

before, expected value: `0`, type: `int`

first_leaf.prefix, expected value: `''`, type: `str`

depth, expected value: `0`, type: `int`

is_decorator, expected value: `True`, type: `bool`

### Expected case 2
#### The values and types of buggy function's parameters
current_line.depth, value: `0`, type: `int`

current_line, value: `Line(depth=0, leaves=[Leaf(153, '# TODO: X')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=None, _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.leaves, value: `[Leaf(153, '# TODO: X')]`, type: `list`

self.previous_defs, value: `[]`, type: `list`

self, value: `EmptyLineTracker(previous_line=Line(depth=0, leaves=[Leaf(AT, '@'), Leaf(NAME, 'property')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(NAME, 'property'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False), previous_after=0, previous_defs=[])`, type: `EmptyLineTracker`

current_line.is_decorator, value: `False`, type: `bool`

current_line.is_def, value: `False`, type: `bool`

current_line.is_class, value: `False`, type: `bool`

self.previous_line, value: `Line(depth=0, leaves=[Leaf(AT, '@'), Leaf(NAME, 'property')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(NAME, 'property'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.is_flow_control, value: `False`, type: `bool`

current_line.is_import, value: `False`, type: `bool`

current_line.is_yield, value: `False`, type: `bool`

#### Expected values and types of variables right before the buggy function's return
max_allowed, expected value: `2`, type: `int`

first_leaf, expected value: `Leaf(153, '# TODO: X')`, type: `Leaf`

before, expected value: `0`, type: `int`

first_leaf.prefix, expected value: `''`, type: `str`

depth, expected value: `0`, type: `int`

is_decorator, expected value: `False`, type: `bool`

### Expected case 3
#### The values and types of buggy function's parameters
current_line.depth, value: `0`, type: `int`

current_line, value: `Line(depth=0, leaves=[Leaf(AT, '@'), Leaf(NAME, 'property')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(NAME, 'property'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.leaves, value: `[Leaf(AT, '@'), Leaf(NAME, 'property')]`, type: `list`

self.previous_defs, value: `[]`, type: `list`

self, value: `EmptyLineTracker(previous_line=Line(depth=0, leaves=[Leaf(153, '# TODO: X')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=None, _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False), previous_after=0, previous_defs=[])`, type: `EmptyLineTracker`

current_line.is_decorator, value: `True`, type: `bool`

current_line.is_def, value: `False`, type: `bool`

current_line.is_class, value: `False`, type: `bool`

self.previous_line, value: `Line(depth=0, leaves=[Leaf(153, '# TODO: X')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=None, _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.is_flow_control, value: `False`, type: `bool`

current_line.is_import, value: `False`, type: `bool`

current_line.is_yield, value: `False`, type: `bool`

#### Expected values and types of variables right before the buggy function's return
max_allowed, expected value: `2`, type: `int`

first_leaf, expected value: `Leaf(AT, '@')`, type: `Leaf`

before, expected value: `0`, type: `int`

first_leaf.prefix, expected value: `''`, type: `str`

depth, expected value: `0`, type: `int`

is_decorator, expected value: `True`, type: `bool`

newlines, expected value: `2`, type: `int`

### Expected case 4
#### The values and types of buggy function's parameters
current_line.depth, value: `0`, type: `int`

current_line, value: `Line(depth=0, leaves=[Leaf(153, '# TODO: Y')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=None, _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.leaves, value: `[Leaf(153, '# TODO: Y')]`, type: `list`

self.previous_defs, value: `[]`, type: `list`

self, value: `EmptyLineTracker(previous_line=Line(depth=0, leaves=[Leaf(AT, '@'), Leaf(NAME, 'property')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(NAME, 'property'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False), previous_after=0, previous_defs=[])`, type: `EmptyLineTracker`

current_line.is_decorator, value: `False`, type: `bool`

current_line.is_def, value: `False`, type: `bool`

current_line.is_class, value: `False`, type: `bool`

self.previous_line, value: `Line(depth=0, leaves=[Leaf(AT, '@'), Leaf(NAME, 'property')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(NAME, 'property'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.is_flow_control, value: `False`, type: `bool`

current_line.is_import, value: `False`, type: `bool`

current_line.is_yield, value: `False`, type: `bool`

#### Expected values and types of variables right before the buggy function's return
max_allowed, expected value: `2`, type: `int`

first_leaf, expected value: `Leaf(153, '# TODO: Y')`, type: `Leaf`

before, expected value: `0`, type: `int`

first_leaf.prefix, expected value: `''`, type: `str`

depth, expected value: `0`, type: `int`

is_decorator, expected value: `False`, type: `bool`

### Expected case 5
#### The values and types of buggy function's parameters
current_line.depth, value: `0`, type: `int`

current_line, value: `Line(depth=0, leaves=[Leaf(153, '# TODO: Z')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(153, '# TODO: Z'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.leaves, value: `[Leaf(153, '# TODO: Z')]`, type: `list`

self.previous_defs, value: `[]`, type: `list`

self, value: `EmptyLineTracker(previous_line=Line(depth=0, leaves=[Leaf(153, '# TODO: Y')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=None, _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False), previous_after=0, previous_defs=[])`, type: `EmptyLineTracker`

current_line.is_decorator, value: `False`, type: `bool`

current_line.is_def, value: `False`, type: `bool`

current_line.is_class, value: `False`, type: `bool`

self.previous_line, value: `Line(depth=0, leaves=[Leaf(153, '# TODO: Y')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=None, _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.is_flow_control, value: `False`, type: `bool`

current_line.is_import, value: `False`, type: `bool`

current_line.is_yield, value: `False`, type: `bool`

#### Expected values and types of variables right before the buggy function's return
max_allowed, expected value: `2`, type: `int`

first_leaf, expected value: `Leaf(153, '# TODO: Z')`, type: `Leaf`

before, expected value: `0`, type: `int`

first_leaf.prefix, expected value: `''`, type: `str`

depth, expected value: `0`, type: `int`

is_decorator, expected value: `False`, type: `bool`

### Expected case 6
#### The values and types of buggy function's parameters
current_line.depth, value: `0`, type: `int`

current_line, value: `Line(depth=0, leaves=[Leaf(AT, '@'), Leaf(NAME, 'property')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(NAME, 'property'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.leaves, value: `[Leaf(AT, '@'), Leaf(NAME, 'property')]`, type: `list`

self.previous_defs, value: `[]`, type: `list`

self, value: `EmptyLineTracker(previous_line=Line(depth=0, leaves=[Leaf(153, '# TODO: Z')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(153, '# TODO: Z'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False), previous_after=0, previous_defs=[])`, type: `EmptyLineTracker`

current_line.is_decorator, value: `True`, type: `bool`

current_line.is_def, value: `False`, type: `bool`

current_line.is_class, value: `False`, type: `bool`

self.previous_line, value: `Line(depth=0, leaves=[Leaf(153, '# TODO: Z')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(153, '# TODO: Z'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.is_flow_control, value: `False`, type: `bool`

current_line.is_import, value: `False`, type: `bool`

current_line.is_yield, value: `False`, type: `bool`

#### Expected values and types of variables right before the buggy function's return
max_allowed, expected value: `2`, type: `int`

first_leaf, expected value: `Leaf(AT, '@')`, type: `Leaf`

before, expected value: `0`, type: `int`

first_leaf.prefix, expected value: `''`, type: `str`

depth, expected value: `0`, type: `int`

is_decorator, expected value: `True`, type: `bool`

newlines, expected value: `2`, type: `int`

### Expected case 7
#### The values and types of buggy function's parameters
current_line.depth, value: `0`, type: `int`

current_line, value: `Line(depth=0, leaves=[Leaf(NAME, 'def'), Leaf(NAME, 'foo'), Leaf(LPAR, '('), Leaf(RPAR, ')'), Leaf(COLON, ':')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(COLON, ':'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.leaves, value: `[Leaf(NAME, 'def'), Leaf(NAME, 'foo'), Leaf(LPAR, '('), Leaf(RPAR, ')'), Leaf(COLON, ':')]`, type: `list`

self.previous_defs, value: `[]`, type: `list`

self, value: `EmptyLineTracker(previous_line=Line(depth=0, leaves=[Leaf(AT, '@'), Leaf(NAME, 'property')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(NAME, 'property'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False), previous_after=0, previous_defs=[])`, type: `EmptyLineTracker`

current_line.is_decorator, value: `False`, type: `bool`

current_line.is_def, value: `True`, type: `bool`

current_line.is_class, value: `False`, type: `bool`

self.previous_line, value: `Line(depth=0, leaves=[Leaf(AT, '@'), Leaf(NAME, 'property')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(NAME, 'property'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.is_flow_control, value: `False`, type: `bool`

current_line.is_import, value: `False`, type: `bool`

current_line.is_yield, value: `False`, type: `bool`

#### Expected values and types of variables right before the buggy function's return
max_allowed, expected value: `2`, type: `int`

first_leaf, expected value: `Leaf(NAME, 'def')`, type: `Leaf`

before, expected value: `0`, type: `int`

first_leaf.prefix, expected value: `''`, type: `str`

depth, expected value: `0`, type: `int`

self.previous_defs, expected value: `[0]`, type: `list`

self, expected value: `EmptyLineTracker(previous_line=Line(depth=0, leaves=[Leaf(AT, '@'), Leaf(NAME, 'property')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(NAME, 'property'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False), previous_after=0, previous_defs=[0])`, type: `EmptyLineTracker`

is_decorator, expected value: `False`, type: `bool`

### Expected case 8
#### The values and types of buggy function's parameters
current_line.depth, value: `1`, type: `int`

current_line, value: `Line(depth=1, leaves=[Leaf(NAME, 'pass')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(NAME, 'pass'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.leaves, value: `[Leaf(NAME, 'pass')]`, type: `list`

self.previous_defs, value: `[0]`, type: `list`

self, value: `EmptyLineTracker(previous_line=Line(depth=0, leaves=[Leaf(NAME, 'def'), Leaf(NAME, 'foo'), Leaf(LPAR, '('), Leaf(RPAR, ')'), Leaf(COLON, ':')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(COLON, ':'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False), previous_after=0, previous_defs=[0])`, type: `EmptyLineTracker`

current_line.is_decorator, value: `False`, type: `bool`

current_line.is_def, value: `False`, type: `bool`

current_line.is_class, value: `False`, type: `bool`

self.previous_line, value: `Line(depth=0, leaves=[Leaf(NAME, 'def'), Leaf(NAME, 'foo'), Leaf(LPAR, '('), Leaf(RPAR, ')'), Leaf(COLON, ':')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(COLON, ':'), _for_loop_variable=False, _lambda_arguments=False), inside_brackets=False)`, type: `Line`

current_line.is_flow_control, value: `False`, type: `bool`

current_line.is_import, value: `False`, type: `bool`

current_line.is_yield, value: `False`, type: `bool`

#### Expected values and types of variables right before the buggy function's return
max_allowed, expected value: `1`, type: `int`

first_leaf, expected value: `Leaf(NAME, 'pass')`, type: `Leaf`

before, expected value: `0`, type: `int`

first_leaf.prefix, expected value: `''`, type: `str`

depth, expected value: `1`, type: `int`

is_decorator, expected value: `False`, type: `bool`

## Summary:

[Your summary here.]