### Analysis
The buggy function `info` is attempting to get the version of the Fish shell by executing a command `echo $FISH_VERSION`. However, in the failing test, the expected version output is `3.5.9` while the actual output from the command is `fish, version 3.5.9`. This discrepancy causes the assertion error.

### Bug
The bug lies in how the command output is being processed. The function is directly extracting the output of the command without parsing it correctly to extract just the version number.

### Fix
To fix the bug, we need to properly parse the command output to extract only the version number. We can do this by splitting the output and extracting the relevant part.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(' ')[-1]  # Extracting only the version number from the output
    return u'Fish Shell {}'.format(version)
```

With this corrected version, the function should now properly extract and return the version number, satisfying the failing test case.