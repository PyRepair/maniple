### Bug Explanation
The bug in the `_partially_consume_prefix` function causes the function to improperly handle the indentation of comments in the input `prefix` string. The function incorrectly checks for the column position and shifts the lines while consuming the prefix string. This leads to incorrect behavior when processing comments that should align with a specific column.

### Bug Location
The bug occurs when handling the logic related to waiting for a new line (`\n`) after encountering a non-space, non-tab character. The function incorrectly resets the state of `wait_for_nl` without properly checking whether the current line's indentation exceeds the specified `column`.

### Bug Fix Strategy
To fix the bug, we need to adjust the logic for determining if the indentation of the comment matches the specified column. We should only reset the state of `wait_for_nl` if the current line's indentation exceeds the `column` value. Additionally, we need to properly handle line concatenation to ensure comments are correctly aligned.

### Corrected Version of the Function
```python
def _partially_consume_prefix(self, prefix, column):
    lines = []
    current_line = ""
    current_column = 0
    wait_for_nl = False
    for char in prefix:
        current_line += char
        if wait_for_nl:
            if char == '\n':
                if current_column <= column:
                    res = ''.join(lines)
                    return res, prefix[len(res):]

                lines.append(current_line)
                current_line = ""
                current_column = 0
                wait_for_nl = False
        elif char == ' ':
            current_column += 1
        elif char == '\t':
            current_column += 4
        elif char == '\n':
            # Reset the column count instead of setting it to 0
            current_column = 1
        else:
            # Check if the column exceeds the specified value
            if current_column >= column:
                wait_for_nl = True
    return ''.join(lines), current_line
```

By applying these corrections to the function's logic, the function should now properly handle comment indentation and satisfy the expected input/output values provided.