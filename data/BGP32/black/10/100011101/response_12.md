### Bug Explanation
The current bug arises from the incorrect handling of the white-space characters (tabs and spaces) in the provided prefix. The function is designed to consume white-space characters until a non-white-space character is encountered, signifying the end of the indentation. However, the function does not handle the case where white-space characters are followed by a newline character ('\n') properly.

### Bug Fix Strategy
To fix the bug, the function needs adjustments to handle the scenario where white-space characters are followed by a newline character. Proper logic should be implemented to handle this case and calculate the necessary values correctly.

### Corrected Function
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
            if current_line.rstrip().endswith('#'):
                wait_for_nl = True
            else:
                current_column = 0
        else:
            wait_for_nl = True
    return ''.join(lines), current_line
```

### Summary
The bug has been fixed by including additional logic to check for the correct conditions when encountering a newline character after white-space characters in the prefix. The corrected function should now pass the failing tests and correctly handle the indentation scenarios provided.