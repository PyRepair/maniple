The bug in the provided function is that it incorrectly handles the case where a new line character `\n` is encountered. It resets the `current_column` value to 0, but it should only reset it if the line is not empty, and the current_column value is less than the specified `column` value.

To fix this bug, we need to ensure that the `current_column` value is only reset when the conditions mentioned above are met. Additionally, we should reset the `current_line` variable when encountering a new line character.

Here is the corrected version of the function:

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
        else:
            if char == '\n':
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

This corrected version should now handle the cases where a new line character is encountered properly, resetting the `current_column` value accordingly.