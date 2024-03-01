### Analysis
- The buggy function `info` is supposed to retrieve the version of the Fish shell by running a command in the shell and then formatting it.
- The error occurs because the retrieved version includes additional text "fish, version" instead of just the version number.
- The `version` variable is not stripped of unnecessary text before including it in the return statement, causing a mismatch with the expected output.

### Bug Fix Strategy
To fix the bug, we need to extract only the version number from the retrieved output before formatting it in the return statement.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extract only the version number from the output
        version = version.replace('fish, version ', '')
        return u'Fish Shell {}'.format(version)
``` 

After applying this fix, the function should correctly extract the version number and provide the expected output "Fish Shell 3.5.9".