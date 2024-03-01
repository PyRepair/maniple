### Analysis
- The `info` function is supposed to retrieve the version of the Fish shell by running a command in the terminal and then formatting the output.
- In the failing test case, the expected output is `'Fish Shell 3.5.9'`, but the actual output includes the entire command as well (`'Fish Shell fish, version 3.5.9'`).
- The issue seems to be with how the `version` variable is populated with the output of the command.
- The `proc.stdout.read().decode('utf-8').strip()` function call is not correctly extracting only the version number from the command output.

### Bug Cause
The `version` variable is capturing the complete output of the command instead of just the version number, resulting in the unexpected output in the test.

### Fix Strategy
To fix this bug, we need to modify the way we extract the version number from the command output. One way to achieve this is by splitting the output string and extracting the relevant portion containing the version number.

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

By splitting the `version` string based on spaces and retrieving the last part, we ensure that only the version number is considered in the final output. This corrected version should address the bug and provide the expected output for the failing test.