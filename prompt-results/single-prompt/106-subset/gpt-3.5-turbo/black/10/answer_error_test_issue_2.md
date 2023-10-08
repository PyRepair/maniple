The issue seems to be with the way comments are handled in the `_partially_consume_prefix` function. The comment line is included in the current line when it should be appended to the list of lines as a separate line. 

To fix this, we need to modify the line `wait_for_nl = True` to `wait_for_nl = True` and add an extra condition to check for comments. If the character is `# ` and the `current_line` is not empty, we append `current_line` to `lines` and reset `current_line` to an empty string.

Here's the modified code snippet:

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
        elif char == '#' and current_line.strip():
            # comment line
            lines.append(current_line)
            current_line = ""
        else:
            # indent is finished
            wait_for_nl = True
    return ''.join(lines), current_line
```

This fix checks if the current line is not empty and if the character is `# `. If so, it appends the current line to `lines` and resets `current_line` to an empty string. This way, the comment lines will be correctly handled as separate lines.

Hopefully, this fix will resolve the issue with indentation for tabulated comments after a dedent.