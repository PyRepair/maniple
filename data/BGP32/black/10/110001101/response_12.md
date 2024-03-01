### Bug Explanation:
The bug in the `_partially_consume_prefix` function arises from incorrect handling of indentation levels and waiting for a new line. When the function encounters a newline character and is waiting for a new line, it does not correctly reset the `current_column` counter to 0. This causes the function to incorrectly track the current column position, leading to incorrect output.

### Bug Fix Strategy:
To fix the bug, we need to ensure that when a newline character is encountered and the function is waiting for a new line, the `current_column` counter is properly reset to 0 before moving on to the next line.

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
                current_line = current_line.lstrip()  # removes leading whitespace
                if current_line and current_column < column:
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

### Changes Made:
1. Added `current_line = current_line.lstrip()` after encountering a newline character and waiting for a new line to remove leading whitespace.
2. Reset `current_column` to 0 when encountering a newline character outside the wait for a new line condition to correctly track the column position.

By making these changes, the function should now correctly handle indentation levels and newline characters, providing the expected output for all the given test cases.