### Analysis:
The `_partially_consume_prefix` function is intended to consume a portion of a given `prefix` string up to a certain `column` number, while considering newline characters for correct indentation handling. 

#### Identified Issues:
1. The logic for updating `current_column` when encountering a newline character is incorrect.
2. The condition for checking if the `current_line` is non-empty and `current_column` is less than the target `column` seems incorrect.

### Bug Explanation:
In the failing test case `'\t# comment\n\t'`, the function fails to properly handle the newline character, leading to incorrect counting of `current_column` and the final `res` result being incorrect.

### Bug Fix Strategy:
1. Update the logic for updating `current_column` when encountering a newline character.
2. Revise the condition for checking if the `current_line` is non-empty and `current_column` is less than the target `column`.

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
                if current_line.strip() and len(current_line.expandtabs()) <= column:
                    res = ''.join(lines)
                    return res, prefix[len(res):]

                lines.append(current_line)
                current_line = ""
                current_column = 0
                wait_for_nl = False
        elif char == ' ':
            current_column += 1
        elif char == '\t':
            current_column += 8 - (current_column % 8)  # Adjust for tab width
        elif char == '\n':
            current_column = 0
        else:
            wait_for_nl = True
    return ''.join(lines), current_line
```

By updating the logic for handling newline characters and adjusting the condition for checking the correct column position, the corrected version of the function should pass the failing test cases and fulfill the expected input/output values.