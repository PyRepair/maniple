### Analysis
The buggy function `info` is trying to get the version of the Fish shell by running a command. The error message indicates that the expected output is not matching the actual output due to an extra string `'fish, '`. This happens because the command `echo $FISH_VERSION` returns a string containing the text `'fish, version'`, which is not desired.

### Bug Cause
1. The `echo $FISH_VERSION` command returns the version string prefixed with `'fish, version'`.
2. The buggy function is not handling this prefix, causing the mismatch in the expected and actual values.

### Bug Fix Strategy
To fix this bug, we need to modify the way we extract the version information from the command output. We should remove the unwanted `'fish, version'` from the output before constructing the final version string.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]  # Extract only the version part
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will extract only the version number part from the command output, resulting in the correct version string `'3.5.9'`.