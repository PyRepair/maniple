### Analysis:
1. The buggy function `info` is attempting to retrieve the version of the Fish shell by running a command and capturing the output using `Popen`. The issue lies in the way the version is extracted from the output.
   
2. The error message indicates that the expected output format is `'Fish Shell 3.5.9'`, but the actual format received is `'Fish Shell fish, version 3.5.9'`. This indicates that the extraction of the version number from the output is incorrect.

### Bug Cause:
The bug is caused by not properly parsing the version string from the command output.

### Bug Fix:
To fix the bug, we need to modify the way we extract the version number from the output. We should remove the unnecessary text `"fish, version"` and only keep the version number.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```