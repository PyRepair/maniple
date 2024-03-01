### Analysis
1. The buggy function `info` is supposed to return the name and version of the current shell (Fish shell). It uses `Popen` to execute a command to retrieve the version of Fish shell.
2. The error message indicates that the returned version includes unnecessary text ("Fish Shell") before the actual version number.
3. The expected output should be in the format of `'Fish Shell 3.5.9'`, but the actual output has an extra part ('Fish Shell '). This indicates that the version is not being extracted correctly.
4. To fix the bug, we need to modify the way the version is extracted from the output of the shell command.
5. By modifying the extraction of the version value, we can obtain the correct output.

### Bug Fix
```python
# Updated version of the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extract only the version number from the output
        version = version.split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
``` 

This fix involves splitting the `version` string by `,` and taking the second part to extract only the version number. This modification ensures that the correct version number is returned in the expected format.