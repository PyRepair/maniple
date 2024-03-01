### Analysis
- The buggy function `info` is intended to return the name and version of the current shell, which in this case is Fish shell.
- The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output includes additional text, leading to the assertion error.
- The runtime values of variables show that the version extracted from the command output includes unnecessary text (`'fish, version 3.5.9'`) instead of just the version number.
- The expected output should only contain the version number (`'3.5.9'`).

### Bug Cause
The bug is caused by the fact that the function is not correctly extracting just the version number from the command output. This leads to additional text being included in the final output, causing the assertion error. The current implementation does not properly handle parsing the version number.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the function to extract only the version number from the output of the `echo $FISH_VERSION` command. This can be achieved by splitting the output by commas and taking the last part, which should be the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version_full = proc.stdout.read().decode('utf-8').strip()
    # Split the output by commas and take the last part
    version = version_full.split(',')[-1].strip()
    return u'Fish Shell {}'.format(version)
```

After making this correction, the function should extract the version number correctly and return the expected output, resolving the failing test.