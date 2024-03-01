### Analysis
The function `info` is intended to retrieve the version of the Fish shell by running a command (`echo $FISH_VERSION`) in the Fish shell. However, the function is not correctly reading the output from the shell command, leading to an incorrect version string being returned.

The error message indicates that the expected output is `'Fish Shell 3.5.9'` but the function is returning `'Fish Shell fish, version 3.5.9'`. This suggests that the `version` variable is not being correctly extracted from the output of the shell command.

The provided runtime values show that the `version` variable contains the string `'fish, version 3.5.9'` instead of just `'3.5.9'`. This discrepancy indicates that the extraction of the version information from the shell command output is incorrect.

### Bug Cause
The bug is caused by the method used to extract the version information from the output of the shell command. The `version` variable is not being properly processed to extract only the version number.

### Fix Strategy
To fix the bug, we need to modify the way the `version` variable is extracted from the output of the shell command. We should parse the output string to obtain only the version number.

### Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(',')[-1].strip()  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```