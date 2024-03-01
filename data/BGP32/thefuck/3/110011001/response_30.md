### Analysis
1. The `info` function is designed to retrieve the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'` using `Popen`.
2. The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`. This suggests that the version string is not being parsed correctly.
3. The `version` variable is being extracted from the output of the `Popen` command, but it seems to include unnecessary text (`'fish, `) before the version number.
4. The bug is likely due to how the version is being extracted from the output of the command.

### Bug Fix Strategy
To fix the bug, we need to properly parse the output of the `Popen` command to extract only the version number without any extra text. We can achieve this by modifying the way the `version` variable is obtained from the output.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()[len('fish, version '):]
        return u'Fish Shell {}'.format(version)
``` 

By modifying the line `version = proc.stdout.read().decode('utf-8').strip()` to extract the version number correctly after `'fish, version '`, we ensure that the correct version is returned by the `info` function. This modification should resolve the bug.