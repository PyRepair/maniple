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
                lines.append(current_line)  # Move adding line to inside the if block
                if current_line.strip() and current_column < column:
                    res = ''.join(lines)
                    return res, prefix[len(res):]

                current_line = ""
                current_column = 0
                wait_for_nl = False
        elif char == ' ':
            current_column += 1
        elif char == '\t':
            current_column += 4
        elif char == '\n':
            lines.append(current_line)  # Add current_line to the lines list
            current_line = ""  # Reset current_line
            current_column = 0  # Reset current_column
            wait_for_nl = False
        else:
            wait_for_nl = True
    lines.append(current_line)  # Add the last line to the lines list
    return ''.join(lines), ""
```