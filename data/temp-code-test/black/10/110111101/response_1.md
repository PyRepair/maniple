### Bug Explanation:
The bug in the `_partially_consume_prefix` function occurs when the function encounters a new line character (`'\n'`) before reaching the expected column width. In such cases, the function should reset the `current_column` counter to 0, but it fails to do so. This leads to incorrect behavior when slicing the input prefix string.

For example, in Case 1, the input prefix `'    # comment\n    '` contains a new line character at index 8, but the function fails to reset `current_column` to 0. This causes the function to return an incorrect sliced prefix, leading to the test failure.

### Bug Fix Strategy:
To fix the bug, we need to ensure that when encountering a new line character (`'\n'`) before the expected column width is reached, the `current_column` counter is reset to 0. This will allow the function to correctly slice the input prefix string based on the expected behavior.

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
                    current_column = 0
            else:
                # indent is finished
                wait_for_nl = True
        return ''.join(lines), current_line
``` 

By resetting `current_column` to 0 when encountering a new line character before the expected column width, the corrected version of the function should now behave as expected and pass the failing test cases.