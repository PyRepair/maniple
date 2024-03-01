### Bug Explanation:
The bug in the `_partially_consume_prefix` function occurs because the condition for checking if the current column is less than the specified `column` value is incorrect. In the case where `wait_for_nl` is True and a new line character is encountered, the code checks if the current line is not empty and the current column is less than the specified `column`. However, this check should be made before adding the current line to the `lines` list because if the condition is not met, the current line should not be considered.

### Bug Fix:
To fix the bug, we need to adjust the condition checking for the current column before appending the current line to the `lines` list. The corrected version of the `_partially_consume_prefix` function is provided below:

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
            # unexpected empty line
            current_column = 0
            wait_for_nl = True
        else:
            # indent is finished
            wait_for_nl = True
            if current_line.strip() and current_column < column:
                res = ''.join(lines)
                return res, prefix[len(res):]
    return ''.join(lines), current_line
``` 

This correction ensures that the condition to check if the current column is less than the specified `column` value is made before adding the current line to the `lines` list, avoiding incorrect results.