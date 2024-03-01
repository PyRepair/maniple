### Bug Explanation:

The bug in the `_partially_consume_prefix` function lies in the logic for handling indents and new lines. The function is incorrectly determining when to add a new line to the `lines` list, resulting in incorrect line breaks in the output.

When a character is a space or tab, the `current_column` is updated accordingly. However, if the character is a new line (`'\n'`), the function incorrectly resets the `current_column` to `0` without adding the current line to the `lines` list. This causes incorrect breaks in the output.

### Bug Fix Strategy:

To fix the bug, we need to ensure that when encountering a new line character (`'\n'`), the current line is added to the `lines` list before resetting the `current_line` and `current_column`.

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
            lines.append(current_line)
            current_line = ""
            current_column = 0
            wait_for_nl = True

    return ''.join(lines), current_line
```

With this correction, the function correctly handles new line characters, ensuring that the `current_line` is added to `lines` before resetting it and `current_column`. This adjustment should allow the function to pass the failing test cases.