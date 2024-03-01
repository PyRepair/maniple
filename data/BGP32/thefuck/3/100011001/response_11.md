### Analysis
The error message indicates that the `info` function is returning `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`. This suggests that the version string obtained from the shell command includes unnecessary text like `'fish, version'`. 

Looking at the implementation of the `info` function, the version string is retrieved from the output of the command `echo $FISH_VERSION`. This output is then stripped and used to construct the final version string. 

In the failing test scenario, the version obtained is `'fish, version 3.5.9'`, which is incorrect due to the extra text. This leads to the assertion failure when comparing with the expected value `'Fish Shell 3.5.9'`.

### Bug
The bug is in how the version string is extracted from the shell output. The current implementation does not handle the additional text `fish, version` before the actual version number.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the logic of extracting the version number to consider the extra text before the version. One way to do this is to split the output of the shell command based on whitespace and take the last part as the version number.

### Corrected Version

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```