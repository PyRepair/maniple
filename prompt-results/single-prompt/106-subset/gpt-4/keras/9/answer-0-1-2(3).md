Let's modify the `process_list_block` function in the following ways:

- Change the `top_level_regex` pattern so that it includes the "-" at the start of each line
- Change the `top_level_replacement` pattern as well so that it adds the appropriate HTML Markdown for a list item
- Parcel the block within `<ul>` and `</ul>` tags to ensure it's correct HTML Markdown.

The corrected function is as follows:

```python
import re 

def process_list_block(docstring, starting_point, section_end, leading_spaces, marker):
    ending_point = docstring.find('\n\n', starting_point)
    block = docstring[starting_point:None if ending_point == -1 else
                                      ending_point - 1]
    docstring_slice = docstring[starting_point:section_end].replace(block, marker)
    docstring = docstring[:starting_point] + docstring_slice + docstring[section_end:]
    lines = block.split('\n')
    lines = [re.sub('^' + ' ' * leading_spaces, '', line) for line in lines]
    top_level_regex = r'^    - ([^\s\\\(]+):(.*)'
    top_level_replacement = r'<li><strong>\1</strong>:\2</li>'
    lines = [re.sub(top_level_regex, top_level_replacement, line) for line in lines]
    lines = [re.sub(r'^    - ', '', line) for line in lines]
    indent = 0
    text_block = False
    for i in range(len(lines)):
        line = lines[i]
        spaces = re.search(r'\S', line)
        if spaces:
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
    block = '<ul>\n' + '\n'.join(lines) + '\n</ul>'
    return docstring, block
```

Now the unordered list will be represented properly in the HTML Markdown. The bullets in the list are expected to show correctly in the HTML documentation.