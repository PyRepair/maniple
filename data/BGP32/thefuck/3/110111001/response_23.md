### Analysis
The buggy function `info` is expected to retrieve the version of the Fish shell by running a command and parsing the output. However, the test is failing because the expected version is not matching the actual version obtained from the command execution.

### Issues
1. The command being executed is incorrect. It should be `fish --version` instead of `echo $FISH_VERSION`.
2. The parsing of the version from the command output is not accurate, resulting in a mismatch.

### Bug Fix Strategy
1. Update the command being executed to get the version of Fish shell.
2. Improve the parsing of the version string to eliminate unnecessary characters.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(' ')[2]
        return u'Fish Shell {}'.format(version)
``` 

By making these changes, the new version of the `info` function should correctly retrieve and format the Fish shell version, passing the failing test case successfully.