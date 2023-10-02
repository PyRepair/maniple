It seems that the issue is caused by the process_list_block function not properly handling the formatting of bullet points when the "Arguments" section is the last block in the docstring. To fix this, you can update the ending_point assignment in the function like this:

```python
def process_list_block(docstring, starting_point, section_end,
                       leading_spaces, marker):
    ending_point = docstring.find('\n\n', starting_point)
    if ending_point == -1:
        ending_point = section_end
    block = docstring[starting_point:ending_point]
    # Place marker for later reinjection.
    docstring_slice = docstring[starting_point:section_end].replace(block, marker)
    docstring = (docstring[:starting_point]
                 + docstring_slice
                 + docstring[section_end:])
    lines = block.split('\n')
    # Remove the computed number of leading white spaces from each line.
    lines = [re.sub('^' + ' ' * leading_spaces, '', line) for line in lines]
    # Usually lines have at least 4 additional leading spaces.
    # These have to be removed, but first the list roots have to be detected.
    top_level_regex = r'^    ([^\s\\\(]+):(.*)'
    top_level_replacement = r'- __\1__:\2'
    lines = [re.sub(top_level_regex, top_level_replacement, line) for line in lines]
    # All the other lines get simply the 4 leading space (if present) removed
    lines = [re.sub(r'^    ', '', line) for line in lines]
    # Fix text lines after lists
    indent = 0
    text_block = False
    for i in range(len(lines)):
        line = lines[i]
        spaces = re.search(r'\S', line)
        if spaces:
            # If it is a list element
            if line[spaces.start()] == '-':
                indent = spaces.start() + 1
                if text_block:
                    text_block = False
                    lines[i] = '\n' + line
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

This change updates the ending_point assignment to use the section_end value when the ending_point is not found by searching for '\n\n'. By doing this, we correctly handle the case when the "Arguments" section is the last block in the docstring.