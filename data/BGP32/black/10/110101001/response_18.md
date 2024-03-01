### Bug Explanation
The bug in the `_partially_consume_prefix` function occurs because the function is not handling the case where no newline character is detected after the indentation is finished (`wait_for_nl` is set to True). This results in the incorrect output where the comment line is not correctly appended to the lines list.

### Bug Fix Strategy
To fix the bug, we need to ensure that when the indentation is finished (`wait_for_nl` is True) and there is no newline character in the prefix, we still append the current_line to lines list and reset the necessary variables.

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
                if current_line.strip() and current_column < column:
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
            current_column = 0
        else:
            wait_for_nl = True
    if wait_for_nl:
        lines.append(current_line)
        current_line = ""
    return ''.join(lines), current_line
```

With this correction, the function should now correctly handle cases where the newline character is missing after the indentation is finished. This should address the bug and make the function pass the failing test cases like the one provided.