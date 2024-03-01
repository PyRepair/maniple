### Analysis
1. The `info` function is intended to return the name and version of the current shell by executing the command `echo $FISH_VERSION` in the Fish shell.
2. The error message shows that the function is returning `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`.
3. The bug is caused by the decoding of the command output and the formatting of the version string.
4. To fix the bug, we need to correctly decode the output and remove any unwanted characters before formatting the version string.
   
### Corrected Version of the Function
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')
        return u'Fish Shell {}'.format(version)
```

After making the above correction, the function should now correctly extract and format the version information, passing the failing test scenario.