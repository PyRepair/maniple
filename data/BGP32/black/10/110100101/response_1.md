### Analysis:
The buggy function `_partially_consume_prefix` is intended to consume a prefix until a certain column value is reached while handling new lines and indentation. However, the current implementation has several issues:
1. The condition in the if statement that checks for column value is incorrect. It should compare `current_column` instead of `current_line`.
2. The logic for handling different characters like spaces, tabs, and newlines is incorrect.
3. The return statement inside the if block is missing a part of the prefix.

### Bug Explanation:
In the failing test case `test_comment_indentation`, the buggy function fails to handle the indentation and new line correctly. It fails to consume the prefix properly leading to mismatched expected values compared to the actual return values.

### Bug Fix Strategy:
1. Update the condition in the if statement to correctly check the `current_column`.
2. Adjust the logic for handling different characters to properly update `current_column` and set `wait_for_nl`.
3. Ensure the concatenated result includes the consumed lines.

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
                    res = ''.join(lines) + current_line
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
            # unexpected empty line
            current_column = 0
        else:
            # indent is finished
            wait_for_nl = True
    return ''.join(lines), current_line
```

By applying these fixes, the corrected function should be able to handle the prefix consumption as expected in the failing test cases.