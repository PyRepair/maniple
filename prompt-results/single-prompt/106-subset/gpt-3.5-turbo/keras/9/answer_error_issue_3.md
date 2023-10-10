The issue with the code is that it is not correctly replacing the bullet points in the docstring. To fix this, we can modify the regular expression pattern used in the `re.sub` function to properly replace the bullet points with the desired format.

Here's the fixed code snippet:

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
                    lines[i] = '\n' + line
                    text_block = False
            elif spaces.start() < indent:
                text_block = True
                indent = spaces.start()
                lines[i] = '\n' + line
        else:
            text_block = False
            indent = 0
    block = '\n'.join(lines)
    
    # Fix bullet points format
    block = re.sub(r'- __([^\n]+)\n', r'- \1\n', block)
    
    return docstring, block
```

In the code snippet above, I added a new line of code after joining the lines to fix the format of the bullet points. The regular expression pattern `r'- __([^\n]+)\n'` matches the bullet point markers followed by the actual content of the bullet point and a new line. The replacement `r'- \1\n'` replaces the bullet point marker and the double underscore with just a bullet point marker. This fixes the formatting issue in the docstring.

Now, when running the test case, the program should no longer throw an assertion error.