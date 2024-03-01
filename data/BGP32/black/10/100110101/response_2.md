### Analysis
The `partially_consume_prefix` function is intended to consume a prefix string up to a certain column limit while handling indentation with spaces and tabs. The bug seems to be related to the handling of the indentation and newline characters, leading to incorrect behavior in some scenarios.

### Bugs
1. When encountering a newline character, the current column should be reset to 0.
2. The condition to check if the current column is less than the specified column is incorrect.
3. Unexpected empty lines are not handled correctly.

### Bug Fixes
1. Reset `current_column` to 0 when encountering a newline character.
2. Adjust the condition for checking the current column against the specified column.
3. Handle unexpected empty lines appropriately.

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
                if current_line.strip() and current_column <= column:  # fixed condition
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
            current_column = 0  # reset current column
        else:
            wait_for_nl = True
    return ''.join(lines), current_line
```

This corrected version should address the issues observed in the failing test cases and fulfill the expected input/output values for the function.