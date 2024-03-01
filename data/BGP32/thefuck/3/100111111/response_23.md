### Analysis
1. The buggy function `info` is trying to retrieve the version of the Fish Shell but is not using the correct command to do so.
2. The failing test `test_info` sets up a mock environment in which the `stdout` read from the `Popen` call returns `'fish, version 3.5.9\n'`.
3. The error message shows that the actual output includes extra information which causes the assertion to fail.
4. To fix the bug, the function should properly extract the version number from the command output.
5. The corrected version should extract only the version number from the output and format it accordingly.

### Bug Cause
The bug in the `info` function arises from parsing the output of the command incorrectly, leading to extra information being included in the version string. This extra information causes the assertion in the test to fail because it doesn't match the expected output.

### Fix Strategy
To fix the bug, we need to modify the code to properly extract and format the version number without including any unnecessary information.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version_number = version.split(',')[1].strip().split()[1]
    return u'Fish Shell {}'.format(version_number)
```

By splitting the version string based on commas and whitespace, we can extract only the version number and format it correctly for the output.