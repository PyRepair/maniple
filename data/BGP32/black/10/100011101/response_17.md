### Bug Explanation:
The current implementation of the `_partially_consume_prefix` function has a bug related to the handling of comments and whitespace. When encountering a comment in the prefix string, it mistakenly considers the comment line as a part of the main code line, causing incorrect output for cases where the comment indentation needs to be preserved.

### Bug Location:
The bug arises in the handling of waiting for a new line after encountering a non-newline character. It fails to correctly identify the end of indentation when a comment is present in the prefix.

### Fix Strategy:
To fix the bug, we need to adjust the logic to correctly handle comment lines and their indentation while trimming the prefix. We should update the conditionals and flags accordingly to handle comments as separate lines rather than part of the main code line. 

### Corrected Version of the Function:
```python
def _partially_consume_prefix(self, prefix, column):
    lines = []
    current_line = ""
    current_column = 0
    wait_for_nl = False
    for char in prefix:
        current_line += char
        if wait_for_nl and char == '\n':
            if column > current_column:
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
        elif char in {'\n', '#'}:
            wait_for_nl = True
        else:
            wait_for_nl = False

    return ''.join(lines), current_line
```

With this correction, the function now correctly handles comments, preserves their indentation, and trims the prefix as expected. This fix should resolve the failing tests and provide the correct output.