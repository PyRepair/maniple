GitHub Bug Title:
Incorrect indentation for tabulated comments after dedent

Description:
When working with codebases that use tabs, Black reformats indentation for comments beyond depth 0 incorrectly after a dedent. This issue only occurs when the input file uses tabs.

Environment:
- Operating system: Ubuntu 18.04
- Python version: 3.6.3
- Black version: master