## Analysis
1. The buggy function `info` is defined within the `Fish` class in the `thefuck.shells.fish` module.
2. The function executes a shell command to get the version of the Fish shell.
3. The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output received from the shell command is `'fish, version 3.5.9'`.
4. The function fails to correctly format the output received from the shell command when generating the final output.
5. The issue seems to be with the formatting of the version string extracted from the shell command.

## Strategy
To fix the bug, we need to modify the way we extract and format the version string obtained from the shell command. We can extract the version number directly from the output and then format it accordingly.

## Fix
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
```

In the corrected version of the `info` function, the extracted version is split based on the comma to isolate the version number. This version number is then returned formatted within the `'Fish Shell {}'` string.