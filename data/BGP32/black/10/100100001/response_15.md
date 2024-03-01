### Analysis:
1. The function `_partially_consume_prefix` is intended to partially consume a prefix based on a given column number.
2. The function reads each character in the prefix and updates the current line and column count accordingly.
3. It checks for specific characters like spaces, tabs, and newlines to determine the end of the indentation and then returns the consumed part of the prefix.
4. The bug is likely related to the logic for handling newlines and updating the current column.
5. The failing test `test_comment_indentation` is related to checking the indentation of comments.

### Bug Explanation:
The bug in the `_partially_consume_prefix` function is related to the handling of newlines. The current implementation does not correctly reset the `current_column` when encountering a newline character. This causes issues with tracking the correct column number, leading to incorrect indentation detection.

### Bug Fix Strategy:
To fix the bug, we need to ensure that the `current_column` is properly reset to 0 when encountering a newline character. This will allow the function to track the correct column number and handle indentation properly.

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
            current_column = 0  # Reset current column on newline
        else:
            wait_for_nl = True

    return ''.join(lines), current_line
```

By resetting the `current_column` to 0 when encountering a newline character, the corrected function should now handle the indentation correctly and pass the failing test `test_comment_indentation`.