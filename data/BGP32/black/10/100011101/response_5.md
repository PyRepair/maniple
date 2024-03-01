### Bug Explanation:
The bug in the `_partially_consume_prefix` function lies in the condition where it checks for the end of indentation and waits for a newline character. When the indentation ends with a comment line (starting with `#`), it fails to correctly handle this scenario. This leads to the unexpected behavior seen in the failing test.

In the failing test case, the prefix `'    # comment\n    '` is not handled correctly. The function is unable to consume the comment line properly, causing the indentation to be part of the actual result, which leads to a mismatch with the expected output.

### Bug Fix Strategy:
To fix the bug, the function needs to correctly handle the indentation ending with a comment line. When encountering a comment line, it should skip consuming it as part of the indentation.

### Corrected Function:

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
            current_column = 0
        elif char == '#':
            # skip comment lines at the end of indentation
            wait_for_nl = True
        else:
            wait_for_nl = True
    return ''.join(lines), current_line
```

By adding a specific condition to handle comment lines at the end of the indentation, the corrected function should now properly consume the prefix and return the expected output for all test cases including the failing one.