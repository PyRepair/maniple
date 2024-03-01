### Bug Explanation:
The bug in the `_partially_consume_prefix` function lies in the line processing logic, specifically in updating the `current_column`. When encountering a newline character, the current_column should be reset to 0, but it is incorrectly being left unchanged. This causes the function to incorrectly assess the column position when generating the output lines.

### Bug Fix Strategy:
To fix the bug, the function should reset `current_column` to 0 when encountering a newline character. Additionally, ensure that the function correctly handles the case when the current line is whitespace-only.

### Corrected Function:
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
            wait_for_nl = True
        else:
            wait_for_nl = True
    return ''.join(lines), current_line
```

By resetting `current_column` to 0 when encountering a newline and updating the logic for determining when to wait for a newline character, the corrected function should now handle line indentation and column positioning correctly.