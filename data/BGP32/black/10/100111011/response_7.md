### Explanation:
The bug in the `_partially_consume_prefix` function occurs because the logic for handling newline characters after an indent is incorrect. When encountering a newline character, the function mistakenly resets the `current_column` to 0, causing the incorrect handling of comments indentation.

### Bug Fix Strategy:
To fix the bug, we need to adjust the logic for handling newline characters. Instead of resetting `current_column` to 0 unconditionally, we should only reset it if no indentation is expected (`wait_for_nl` is False).

### Corrected Version of the Function:
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
            wait_for_nl = True
        else:
            # indent is finished
            wait_for_nl = True
    return ''.join(lines), current_line
``` 

After applying this fix, the function should handle the indentation of comments correctly according to the provided test case and the GitHub issue.