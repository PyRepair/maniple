### Bug Explanation
The bug in the `_maybe_empty_lines` function lies in the condition `self.previous_line.is_import`. The code is attempting to access the `is_import` attribute of the `self.previous_line` object, assuming that it would be a boolean value indicating whether the previous line is an import. However, the `Line` class does not have an `is_import` attribute. Instead, the desired behavior is to call the `is_import` function passing the `self.previous_line` object as an argument to determine if it is an import line.

### Bug Fix Strategy
To fix the bug:
- Remove the incorrect reference `self.previous_line.is_import` and replace it with a call to the `is_import` function with `self.previous_line` as an argument.
- Update the `is_import` function to correctly determine if a given `Leaf` object represents an import.

### Corrected Version of the Function
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
        and is_import(self.previous_line)
        and not is_import(current_line)
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

By making the changes as described above, the function should now correctly handle the condition checking for imports and pass the failing test cases.