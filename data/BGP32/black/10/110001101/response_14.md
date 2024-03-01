### Bug Explanation
The bug in the `_partially_consume_prefix` function occurs when the code encounters a newline character (`\n`) before reaching the target column. In this scenario, if the current line is not empty and the current column is less than the target column, the function should extract the consumed part of the prefix up to that point and return it along with the remaining part of the prefix.

However, the current implementation fails to handle this situation properly. When encountering a newline character, it resets the current column count to 0, essentially discarding the consumed characters up to that point.

### Bug Fix Strategy
To fix the bug, we need to modify the condition for handling newline characters. Instead of resetting the current column count to 0, we should only reset it if the current line is not empty and the current column is less than the target column.

### Corrected Function
```python
class Driver(object):

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
                if current_line.strip() and current_column < column:
                    res = ''.join(lines)
                    return res, prefix[len(res):]
                lines.append(current_line)
                current_line = ""
                current_column = 0
            else:
                wait_for_nl = True
        return ''.join(lines), current_line
``` 

With this correction, the function will correctly extract and return the consumed part of the prefix up to the target column when encountering a newline character before reaching the target column.