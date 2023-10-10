To fix the bug, we need to replace the `compat_chr` function with a modified version that handles values greater than 0x10FFFF.

def _htmlentity_transform(entity):
    """Transforms an HTML entity to a character."""
    # Known non-numeric HTML entity
    if entity in compat_html_entities.name2codepoint:
        return compat_chr(compat_html_entities.name2codepoint[entity])
    mobj = re.match(r'#(x[0-9a-fA-F]+|[0-9]+)', entity)
    if mobj is not None:
        numstr = mobj.group(1)
        if numstr.startswith('x'):
            base = 16
            numstr = '0%s' % numstr
        else:
            base = 10
        num = int(numstr, base)
        if num > 0x10FFFF:
            return '?'
        return unichr(num)
    return '?'