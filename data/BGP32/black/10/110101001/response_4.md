### Bug Explanation:
The bug in the `_partially_consume_prefix` function lies in the handling of the logic to check for newlines and update `current_column` correctly. The issue occurs when the function encounters a newline character (`'\n'`). In such cases, the `current_column` should be reset to 0, but the current implementation is not properly resetting the `current_column` value, leading to incorrect indentation counting.

### Bug Fix:
To fix the bug, we need to adjust the logic specifically when encountering a newline character in the input string `prefix`. We should reset the `current_column` to 0 when encountering a newline character to correctly track the indentation. Additionally, we need to ensure that the `lines` list is properly updated with the current line when we encounter a newline and also reset `current_line` for the next line.

### Corrected Version:
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
            lines.append(current_line)
            current_line = ""
        else:
            wait_for_nl = True

    return ''.join(lines), current_line
```

With these corrections, the `current_column` is correctly reset to 0 when encountering a newline, and the `lines` list is updated accordingly to handle newline characters properly for correct indentation tracking.