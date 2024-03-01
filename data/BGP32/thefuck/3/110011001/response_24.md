### Analysis
- The function `info` is supposed to return the name and version of the current shell by running a command in the Fish shell.
- The error message indicates that the expected output is 'Fish Shell 3.5.9', but the actual output includes the undesired 'fish, version' part.
- The issue seems to be with the way the version is extracted from the output of the command executed in the Fish shell.
- The `version` variable contains the entire output of the command, including 'fish, version'.
- The incorrect comparison arises due to the mismatch in the expected and actual output of the function.

### Bug Fix Strategy
To fix the bug, we need to extract only the version number from the output of the command and format it as 'Fish Shell {version}' before returning.

### Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The corrected class with the fixed function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[-1]
        return u'Fish Shell {}'.format(version)
```