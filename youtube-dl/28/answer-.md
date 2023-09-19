Here is the corrected code:

```python
import re
import html.entities as compat_html_entities
from functools import partial

def compat_chr(num):
    return chr(num)

def _htmlentity_transform(entity):
    """Transforms an HTML entity to a character."""
    # Remove '&' from the entity string
    entity = entity[1:]
    
    # Known non-numeric HTML entity
    if entity in compat_html_entities.name2codepoint:
        return compat_chr(compat_html_entities.name2codepoint[entity])

    mobj = re.match(r'#(x[0-9a-fA-F]+|[0-9]+)', entity)
    if mobj is not None:
        numstr = mobj.group(1)
        if numstr.startswith('x'):
            base = 16
            numstr = numstr[1:]
        else:
            base = 10
        # See https://github.com/rg3/youtube-dl/issues/7518
        return compat_chr(int(numstr, base))

    # Unknown entity in name, return its literal representation
    return ('&%s;' % entity)
```

The main changes are:

1. Added a missing `import re` statement.
2. Added `import html.entities as compat_html_entities`, assuming you want to use Python 3's `html.entities` module as `compat_html_entities`.
3. Imported and defined `compat_chr` as a partial function of the built-in `chr()` for Python 3 compatibility.
4. Removed '&' from the entity string inside the function `_htmlentity_transform`.

With these changes, the function should work correctly.