### Bug Analysis
The bug in the `info` function lies in the way it retrieves the Fish Shell version from the output of the executed command. The current implementation reads the output with `proc.stdout.read().decode('utf-8').strip()` and then tries to format it as 'Fish Shell {}'.format(version). However, the output obtained includes the string 'fish, version' before the actual version number, causing the mismatch in the expected and actual output.

### Bug Explanation
The current implementation of the function incorrectly reads the version string as 'fish, version 3.5.9' instead of just '3.5.9'. This extra prefix 'fish, version' causes the formatted output to differ from the expected 'Fish Shell 3.5.9'.

### Bug Fix
To fix this bug, we need to extract only the version number from the output and then format the output string. We can achieve this by splitting the version string obtained by space and taking the last element after splitting.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```