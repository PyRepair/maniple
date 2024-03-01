### Analysis
The buggy function `info` is trying to get the version of the Fish shell by executing a shell command. However, the issue lies in reading the output of the subprocess incorrectly. The `proc.stdout.read()` method returns a byte string, and calling `decode('utf-8')` on it is necessary to convert it to a regular string.

### Bug
The bug in the current implementation is that it doesn't correctly decode the byte string obtained from `proc.stdout.read()` into a regular string before assigning it to the `version` variable.

### Fix
To fix the bug, we need to decode the byte string obtained from `proc.stdout.read()` using the `utf-8` encoding before stripping it and assigning it to the `version` variable.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```