You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

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



The test error on command line is following:

Expected tree:
file_input
  if_stmt
    NAME 'if'
    NUMBER ' ' '1'
    COLON ':'
    suite
      NEWLINE '\n'
      INDENT ''
      if_stmt
        NAME '    ' 'if'
        NUMBER ' ' '2'
        COLON ':'
        suite
          NEWLINE '\n'
          INDENT ''
          simple_stmt
            NAME '        ' 'pass'
            NEWLINE '\n'
          /simple_stmt
          DEDENT '        # comment\n' ''
        /suite
      /if_stmt
      simple_stmt
        NAME '    ' 'pass'
        NEWLINE '\n'
      /simple_stmt
      DEDENT ''
    /suite
  /if_stmt
  ENDMARKER ''
/file_input
Actual tree:
file_input
  if_stmt
    NAME 'if'
    NUMBER ' ' '1'
    COLON ':'
    suite
      NEWLINE '\n'
      INDENT ''
      if_stmt
        NAME '    ' 'if'
        NUMBER ' ' '2'
        COLON ':'
        suite
          NEWLINE '\n'
          INDENT ''
          simple_stmt
            NAME '        ' 'pass'
            NEWLINE '\n'
          /simple_stmt
          DEDENT ''
        /suite
      /if_stmt
      simple_stmt
        NAME '    # comment\n    ' 'pass'
        NEWLINE '\n'
      /simple_stmt
      DEDENT ''
    /suite
  /if_stmt
  ENDMARKER ''
/file_input
======================================================================
FAIL: test_comment_indentation (tests.test_black.BlackTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/black:10/tests/test_black.py", line 517, in test_comment_indentation
    self.assertFormatEqual(fs(contents_tab), contents_spc)
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/black:10/tests/test_black.py", line 156, in assertFormatEqual
    self.assertEqual(expected, actual)
AssertionError: 'if 1:\n    if 2:\n        pass\n        # comment\n    pass\n' != 'if 1:\n    if 2:\n        pass\n    # comment\n    pass\n'
  if 1:
      if 2:
          pass
-         # comment
? ----
+     # comment
      pass


----------------------------------------------------------------------
Ran 1 test in 0.005s

FAILED (failures=1)



The raised issue description for this bug is:
Indentation is incorrectly changed for tabulated comments after a dedent

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