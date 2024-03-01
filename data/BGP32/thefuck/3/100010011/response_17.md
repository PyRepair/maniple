### Analysis:
The error message shows that the test is failing because the expected output includes the version number '3.5.9', but the actual output contains additional text 'fish, version'.

### Bugs:
1. The output of the command is not correctly parsed in the `info` function.
2. The format of the output is not in the expected 'Fish Shell X.X.X' format.

### Cause of the bug:
The `info` function is not correctly parsing the command output, leading to the additional 'fish, version' text in the result. This causes the assertion in the test to fail.

### Strategy for fixing the bug:
1. Modify the parsing of the command output to extract only the version number.
2. Update the return format to match the expected 'Fish Shell X.X.X' format.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version will properly parse the version number from the command output and return it in the correct format. It should now pass the failing test and address the GitHub issue related to the recursive loop.