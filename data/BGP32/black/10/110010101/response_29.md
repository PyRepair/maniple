### Analysis
The function `_partially_consume_prefix` is intended to consume a prefix string until a certain column value is reached based on indentation rules. However, there seems to be a bug in the logic that causes it to incorrectly handle the case of consuming lines until a specific column value is reached after encountering a newline character.

### Bug Explanation
1. When the function encounters a newline character `'\n'`, it resets the `current_column` to 0 but fails to handle the scenario where it should skip empty lines.
2. If a newline character is encountered after reaching the desired `column`, the function should consume the rest of the prefix string while ignoring any additional indentation before the next non-white space character.
3. The bug arises from not resetting the `current_column` to 0 when encountering an empty line (`char == '\n'`) and continuing to add characters to the `current_line`.

### Bug Fix Strategy
1. Modify the check for encountering a newline character to reset `current_column` to 0 if the line is not empty.
2. Implement handling for situations where a newline character is encountered after reaching the desired column, ensuring that only necessary non-white space characters are added to the `current_line`.
3. Update the logic to handle edge cases efficiently and correctly consume the prefix string as intended.

### Corrected Version
```python
def _partially_consume_prefix(self, prefix, column):
    lines = []
    current_line = ""
    current_column = 0
    wait_for_nl = False
    for char in prefix:
        if char == '\n':
            # Handle empty lines
            if current_line.strip():
                res = ''.join(lines)
                return res, prefix[len(res):]
                
            current_line = ""
            current_column = 0
            wait_for_nl = False
        elif wait_for_nl:
            if char == '\n':
                if current_line.strip() and current_column < column:
                    res = ''.join(lines)
                    return res, prefix[len(res):]
                lines.append(current_line)
                current_line = ""
                current_column = 0
                wait_for_nl = False
        else:
            if char == ' ':
                current_column += 1
            elif char == '\t':
                current_column += 4
            else:
                # indent is finished
                wait_for_nl = True
            current_line += char

    return ''.join(lines), current_line
``` 

The corrected version of the `_partially_consume_prefix` function should now handle the edge cases and scenarios described in the expected values of the test cases.