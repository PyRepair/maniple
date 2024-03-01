### Bug Explanation
The bug in the `_partially_consume_prefix` function lies in the handling of indentation levels. When encountering a newline character (`\n`) before reaching the specified `column` count, it should check if the current line is non-empty before resetting the current column count. However, in the current implementation, it resets the column count for any newline character encountered, leading to incorrect indentation calculation.

### Bug Fix Strategy
To fix the bug, we need to ensure that the column count is only reset when the current line is not empty and the column count is less than the specified `column`. Additionally, we need to address the indentation calculation after encountering a newline in the final line of the prefix input.

### Corrected Function

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
            if current_line.strip() and current_column < column:
                res = ''.join(lines)
                return res, prefix[len(res):]

            lines.append(current_line)
            current_line = ""
            current_column = 0
        else:
            wait_for_nl = True
    return ''.join(lines), current_line
```

The corrected function ensures that the column count is only reset when necessary, addressing the bug in the original implementation. By making sure the empty lines are handled correctly, the function now accurately partially consumes the prefix up to the specified column count.