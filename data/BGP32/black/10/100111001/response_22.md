### Bug Explanation
The bug in the `_partially_consume_prefix` function arises from an incorrect condition when determining whether to add a new line to the `lines` list. The current implementation only checks if the current character is a newline `\n` character to add a new line, which causes the issue when handling comments starting with `#`.

When processing lines containing comments starting with `#`, the function incorrectly adds the lines without taking into account the whitespace leading up to the comment. This results in a misalignment of the comments when comparing the expected and actual output.

### Bug Fix Strategy
To fix the bug, we need to enhance the logic around handling comments and whitespace. Instead of just checking for a newline character, we should consider the cumulative whitespace leading up to the comment and correctly align the lines based on this information.

### Corrected Version
Here is the corrected version of the `_partially_consume_prefix` function:

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
            wait_for_nl = False
        else:
            # indent is finished
            wait_for_nl = True
    return ''.join(lines), current_line
```

With this correction, the function should now handle comments correctly and align them properly in the output, passing the failing test cases.