### Bug Explanation
The bug in the `_partially_consume_prefix` function is causing issues with indentation during comment handling. The function is incorrectly determining when an indentation block ends, leading to discrepancies in the output compared to the expected values. The issue arises from incorrectly handling the logic for when to wait for a new line based on the current character being processed.

In the failing test, we can see that the function fails to correctly handle the comment indentation, resulting in incorrect output. This discrepancy is due to the incorrect handling of when to expect a new line based on the current character being processed.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function correctly identifies when to wait for a new line in the context of indentation and comment handling. This can be achieved by adjusting the logic that triggers the waiting for a new line. Specifically, we need to properly identify when the indent block for a line ends and reset the relevant variables accordingly.

### Corrected Function
Here is the corrected version of the `_partially_consume_prefix` function:

```python
def _partially_consume_prefix(self, prefix, column):
    lines = []
    current_line = ""
    current_column = 0
    wait_for_nl = False
    for char in prefix:
        current_line += char
        if wait_for_nl and char == '\n':
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
        elif not wait_for_nl:
            # indent is finished
            wait_for_nl = True
    return ''.join(lines), current_line
```

With this correction, the function should now handle the comment indentation correctly and pass the failing test cases.