### Analysis
The buggy function `info` is attempting to retrieve the version of the Fish shell by executing a command and reading the output. However, the issue lies in how the version is extracted from the output, resulting in the incorrect output.

- The `version` variable currently contains the output `'fish, version 3.5.9'` instead of just the version number `'3.5.9'`.
- The return statement formats the version incorrectly by appending `'Fish Shell '` to the version string.

### Bug Cause
The bug is caused by not properly parsing the version number from the output of the command. The incorrect output stems from including unnecessary text in the version string and the incorrect formatting of the final output.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the way we extract the version number from the command output. We should only extract the version number itself and revise the formatting of the final output string.

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

This corrected version of the `info` function now correctly extracts and formats the version number from the Fish shell's output.