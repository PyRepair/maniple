You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

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
        return compat_chr(int(numstr, base))



The test error on command line is following:

======================================================================
ERROR: test_unescape_html (test.test_utils.TestUtil)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/youtube-dl:28/test/test_utils.py", line 214, in test_unescape_html
    self.assertEqual(unescapeHTML('&#2013266066;'), '&#2013266066;')
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/youtube-dl:28/youtube_dl/utils.py", line 411, in unescapeHTML
    r'&([^;]+);', lambda m: _htmlentity_transform(m.group(1)), s)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/re.py", line 194, in sub
    return _compile(pattern, flags).sub(repl, string, count)
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/youtube-dl:28/youtube_dl/utils.py", line 411, in <lambda>
    r'&([^;]+);', lambda m: _htmlentity_transform(m.group(1)), s)
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/youtube-dl:28/youtube_dl/utils.py", line 399, in _htmlentity_transform
    return compat_chr(int(numstr, base))
ValueError: chr() arg not in range(0x110000)

----------------------------------------------------------------------
Ran 1 test in 0.006s

FAILED (errors=1)



The test source code is following:

    def test_unescape_html(self):
        self.assertEqual(unescapeHTML('%20;'), '%20;')
        self.assertEqual(unescapeHTML('&#x2F;'), '/')
        self.assertEqual(unescapeHTML('&#47;'), '/')
        self.assertEqual(unescapeHTML('&eacute;'), 'é')
        self.assertEqual(unescapeHTML('&#2013266066;'), '&#2013266066;')


