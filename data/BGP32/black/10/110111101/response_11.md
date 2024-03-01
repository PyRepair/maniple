### Bug Explanation:
The bug in the `_partially_consume_prefix` function occurs when the function encounters a newline character (`'\n'`) after waiting for a newline (`wait_for_nl = True`). In this situation, the function should check if the current column count is less than the specified column limit and then add the current line to the `lines` list. However, the function incorrectly adds the current line before checking the column count, leading to incorrect behavior.

### Bug Fix Strategy:
To fix the bug, we need to ensure that the current line is added to the `lines` list only after checking if the column count is less than the specified limit. This way, the function will correctly handle the indentation check and correctly format the output.

### Corrected Version of the Function:
```python
class Driver(object):
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
                if current_column < column:
                    res = ''.join(lines)
                    return res, prefix[len(res):]
                lines.append(current_line)
                current_line = ""
                current_column = 0
                wait_for_nl = False
            else:
                wait_for_nl = True
        return ''.join(lines), current_line
```

After implementing this correction, the `_partially_consume_prefix` function should now correctly handle the indentation check when encountering newline characters, resolving the bug identified in the failing test cases.