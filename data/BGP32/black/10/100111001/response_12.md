### Bug Explanation:
The bug in the `_partially_consume_prefix` function is in the condition that checks if `current_column` is less than `column`. The intention is to cut off the prefix string at the specified `column`, but the logic is incorrect. The condition is checking if `current_column < column`, but it should be checking if `current_column >= column` to correctly handle the indentation.

### Bug Fix:
To fix the bug, modify the condition `if current_column < column:` to `if current_column >= column:`.

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
                if current_line.strip() and current_column >= column:
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
    return ''.join(lines), current_line
``` 

After modifying the condition as suggested, the function should correctly handle the indentation and pass the failing test cases.