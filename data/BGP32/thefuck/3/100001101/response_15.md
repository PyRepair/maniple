### Analysis
The buggy function is trying to retrieve the version of the Fish shell by running a command and capturing the output. The issue seems to be related to how the version is being extracted from the command output. The function is returning the entire string `'fish, version 3.5.9'` instead of just `'3.5.9'`.

### Bug
The bug lies in how the function is extracting the version from the command output. It is not properly parsing the output to only retrieve the version number.

### Fix
To fix the bug, we need to properly extract only the version number from the output of the command.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

This corrected version of the function extracts the version number by splitting the output on spaces and taking the last element, which should be the version number.