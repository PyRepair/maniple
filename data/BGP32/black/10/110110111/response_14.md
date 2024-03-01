### Bug Analysis:
1. The `_partially_consume_prefix` function is responsible for partially consuming a given prefix string.
2. It processes each character of the prefix string based on certain conditions such as spaces, tabs, and new lines.
3. The bug occurs when a comment line is encountered after an indent and then a dedent. The comment line's indentation gets wrongly adjusted.
4. The failing test case `test_comment_indentation` confirms this issue by comparing the expected and actual reformatted code.

### Bug Explanation:
1. In the failing test case `test_comment_indentation`, the comment line is not formatted correctly after a dedent.
2. The expected and actual reformatted code lines differ only in the indentation of the comment line.
3. This discrepancy causes the assertion error since the expected and actual strings don't match in terms of indentation.

### Bug Fix Strategy:
1. Identify the section of the code responsible for adjusting the comment line's indentation.
2. Ensure that after a dedent, the following comment line retains the same relative indentation.
3. Make necessary adjustments to the conditions or logic in the `_partially_consume_prefix` function to handle comment line indentation correctly.

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
                if current_line.strip() and current_column < column:
                    res = ''.join(lines)
                    return res + current_line, prefix[len(res + current_line):]
                    
                lines.append(current_line)
                current_line = ""
                current_column = 0
                wait_for_nl = False
        elif char == ' ':
            current_column += 1
        elif char == '\t':
            current_column += 4
        elif char == '\n':
            # Check for comment line after dedent and adjust indentation
            if current_line.strip().startswith('#'):
                if current_column != column:
                    diff = column - current_column
                    current_line = ' ' * diff + current_line.lstrip()
                    
            current_column = 0
        else:
            if current_line.strip().startswith('#'):
                # Keep the relative indentation of comment lines
                current_line = ' ' * column + current_line.lstrip()
            wait_for_nl = True
            
    return ''.join(lines), current_line
```

### Correction Rationale:
1. The corrected version adjusts the indentation of comment lines after a dedent to match the expected behavior.
2. When encountering a comment line after a dedent, the function ensures it retains the relative indentation specified by the `column` parameter.
3. Additional conditional checks and indentation adjustments are added to handle comment lines correctly after dedents.

By applying these corrections, the `_partially_consume_prefix` function should now pass the failing test case and rectify the indentation issue reported in the GitHub issue.