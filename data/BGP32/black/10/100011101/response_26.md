### Bug Explanation
The bug in the `_partially_consume_prefix` function stems from the way the condition for handling newlines is structured. In the original code, the condition for detecting a newline and checking if the current column is less than the provided column value is placed inside the block that checks for whitespaces. This results in premature newline handling and incorrect behavior when encountering comments that should be indented. 

### Bug Fix Strategy
To fix the bug, we need to ensure that the check for a newline and the comparison with the column value happen outside the whitespace checks. This will allow the function to correctly handle comments' indentation.

### Corrected Code
```python
def _partially_consume_prefix(self, prefix, column):
    lines = []
    current_line = ""
    current_column = 0
    wait_for_nl = False
    for char in prefix:
        current_line += char
        if char == ' ':
            current_column += 1
        elif char == '\t':
            current_column += 4
        elif char == '\n':
            if wait_for_nl:
                if current_line.strip() and current_column < column:
                    res = ''.join(lines)
                    return res, prefix[len(res):]

                lines.append(current_line)
                current_line = ""
                current_column = 0
                wait_for_nl = False
            current_column = 0
        else:
            wait_for_nl = True

    return ''.join(lines), current_line
```

By reorganizing the conditions in this corrected version, the function should now handle comments' indentation correctly and pass the failing test cases.