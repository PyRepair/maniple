# Prompt Github issue info based facts

Your task is to determine whether the provided fact would be useful and relevant to fixing the buggy function.
Assume you know the buggy function source code,
does following github issue message helps to fix the bug?

The buggy function's source code is:
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
        else:
            # indent is finished
            wait_for_nl = True
    return ''.join(lines), current_line

```

The github issue message is:
# A GitHub issue title for this bug
```text
Indentation is incorrectly changed for tabulated comments after a dedent
```

## The associated detailed issue description
```text
Operating system: Ubuntu 18.04
Python version: 3.6.3
Black version: master

Thank you @ambv for this library. When trying to run this on a codebase that uses tabs, indentation for comments past depth 0 is changed incorrectly after a dedent. Sample input (NB tabs):

if 1:
	if 2:
		pass
	# This comment should be indented the same as the next line
	pass
Black reformats this to:

if 1:
    if 2:
        pass
        # This comment should be indented the same as the next line
    pass
Note that this only happens when the input file uses tabs.
```



Your response should follow this format:
Justification: <your justification>
Conclusion: either "Yes." or "No."


