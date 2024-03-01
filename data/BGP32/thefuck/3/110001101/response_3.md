### Analysis:
The buggy function is attempting to retrieve the version of the Fish Shell by running a command through subprocess Popen. The issue seems to be with the way the version is being extracted from the command output.

### Error:
The bug is in the line `version = proc.stdout.read().decode('utf-8').strip()`. It reads the entire output as a string and then decodes it, causing 'Fish Shell' to be prefixed to the version number.

### Fix:
To fix the bug, we need to modify how we extract the version number from the output of the command.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')
    return u'Fish Shell {}'.format(version)
``` 

This corrected version reads the output, decodes it, and then strips any leading or trailing whitespaces. It then removes the prefix 'fish, version ' from the version number before returning the correct format 'Fish Shell version_number'.