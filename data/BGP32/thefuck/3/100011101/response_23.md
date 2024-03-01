### Analysis
- The buggy function is supposed to return the name and version of the current shell by running a command in the Fish shell.
- The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output includes the version with additional text `'fish, version 3.5.9'`.
- The runtime values show that the `version` variable includes the additional text `'fish, version'`.
- The issue seems to be with extracting only the version number from the output of the command.

### Bug Cause
The bug is caused by not extracting just the version number from the output of the `echo $FISH_VERSION` command, resulting in the additional text being included in the returned version.

### Fix Strategy
To fix the bug, the function should extract only the version number from the output of the command by removing any additional text and returning only the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(',')[1].strip())
```

In the corrected version above, the `version` variable is split by `,`, and the second part (index 1) is extracted, which should contain only the version number. This modification ensures that the additional text is removed, and only the version number is returned.