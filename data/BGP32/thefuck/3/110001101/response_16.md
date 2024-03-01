### Analysis
The buggy function `info` is trying to get the version of the Fish shell by executing a command and reading the output. However, there are issues with how the output is being handled. It seems like the version is being extracted from the output incorrectly which results in the incorrect return value.

### Bug
The bug lies in how the version information is being extracted from the output of the command. The function is trying to extract the version from the string `'fish, version 3.5.9'` but it should only return `'3.5.9'`.

### Fix
To fix the bug, we need to modify how the version information is extracted from the output of the command and return only the version number.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
``` 

This corrected version will now properly extract only the version number and return it as `'Fish Shell 3.5.9'` as expected.