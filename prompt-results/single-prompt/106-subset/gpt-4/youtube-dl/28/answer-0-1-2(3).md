You need to modify the _htmlentity_transform function to handle the case when the given character code is not in the valid range for the chr() function. You can achieve this by adding a try-except block to catch the ValueError and return the original entity if chr() fails.

Here's the fixed code:

```python
import re
import html.entities as compat_html_entities
from functools import partial

def _htmlentity_transform(entity):
    """Transforms an HTML entity to a character."""
    # Known non-numeric HTML entity
    if entity in compat_html_entities.name2codepoint:
        return chr(compat_html_entities.name2codepoint[entity])
    mobj = re.match(r'#(x[0-9a-fA-F]+|[0-9]+)', entity)
    if mobj is not None:
        numstr = mobj.group(1)
        if numstr.startswith('x'):
            base = 16
            numstr = '0%s' % numstr
        else:
            base = 10
        try:
            return chr(int(numstr, base))
        except ValueError:
            return '&%s;' % entity

def unescapeHTML(s):
    return re.sub(r'&([^;]+);', lambda m: _htmlentity_transform(m.group(1)), s)

# Test function
def test_unescape_html():
    assert unescapeHTML('%20;') == '%20;'
    assert unescapeHTML('&#x2F;') == '/'
    assert unescapeHTML('&#47;') == '/'
    assert unescapeHTML('&eacute;') == 'иж'
    assert unescapeHTML('&#2013266066;') == '&#2013266066;'

# Run the test
test_unescape_html()
```

Now the test_unescape_html function should pass without any errors.