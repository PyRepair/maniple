To fix the bug, we need to correct the formatting of the bullet points in the `process_list_block` function. Specifically, we need to modify the regular expression used to detect and replace the bullet points.

Here's the fixed code:

```python
import re

def process_list_block(docstring, starting_point, section_end,
                       leading_spaces, marker):
    ending_point = docstring.find('\n\n', starting_point)
    block = docstring[starting_point:(None if ending_point == -1 else
                                      ending_point - 1)]
    # Place marker for later reinjection.
    docstring_slice = docstring[starting_point:section_end].replace(block, marker)
    docstring = (docstring[:starting_point]
                 + docstring_slice
                 + docstring[section_end:])
    lines = block.split('\n')
    # Remove the computed number of leading white spaces from each line.
    lines = [re.sub('^' + ' ' * leading_spaces, '', line) for line in lines]

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

    # Insert bullet points for list elements
    lines = [re.sub(r'^( *)-', r'\1- ', line) for line in lines]

    # Replace marker with fixed block
    docstring_slice = '\n'.join(lines)
    docstring = docstring.replace(marker, docstring_slice)

    return docstring, docstring_slice
```

This code adds a new step after fixing the text lines after lists to insert bullet points for list elements. The regular expression `r'^( *)-'` selectively matches lines starting with any number of spaces followed by a hyphen. It replaces the hyphen with a hyphen followed by a space, effectively adding the bullet point.

With this fix, the program should pass the failed test without affecting other successful tests.