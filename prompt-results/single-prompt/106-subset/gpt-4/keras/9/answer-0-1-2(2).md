The issue seems to be occurring in the for-loop where it is trying to format the lines. The issue is that it is currently turning list elements into new lines. We should instead create the new line before the list element. Therefore, the conditional check for if the line is a list element should include a new line before the list item instead of after and the condition for the text block should include the new line before the text block and not after.

Replace the current for-loop with the following:

```python
    for i in range(len(lines)):
        line = lines[i]
        spaces = re.search(r'\S', line)
        if spaces:
            # If it is a list element
            if line[spaces.start()] == '-':
                if text_block:
                    text_block = False
                lines[i] = '\n' + line
                indent = spaces.start() + 1
            elif spaces.start() < indent:
                text_block = True
                indent = spaces.start()
                lines[i] = '\n' + line
        else:
            text_block = False
            indent = 0
    block = '\n'.join(lines)
    return docstring, block
```

With this change, the list elements and text blocks are formatted properly.