### Bug Explanation
The bug in the `_partially_consume_prefix` function lies in how the lines are being handled when encountering a newline character. The function is not correctly updating the `lines` list with the current line when encountering a newline character. This leads to incorrect slicing of the prefix in the `res` variable, resulting in the function returning the wrong values.

### Bug Fix Strategy
To fix the bug, we need to update the logic within the function to properly handle constructing the lines list and updating the `res` variable. Specifically, when encountering a newline character, the current line should be added to the lines list, and the `current_column` should be reset to 0.

### Corrected Code
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
                lines.append(current_line)
                current_line = ""
                current_column = 0
            else:
                wait_for_nl = True
        return ''.join(lines), current_line
```

By making these modifications to the `_partially_consume_prefix` function, it should now correctly handle creating the lines list and updating the `res` variable, passing all the provided test cases.