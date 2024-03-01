### Analysis
1. The buggy function `info` is supposed to return the name and version of the current shell by executing a command in the Fish shell.
2. The error occurs when comparing the expected output `'Fish Shell 3.5.9'` with the actual output `'Fish Shell fish, version 3.5.9'`.
3. The error is caused by the incorrect format of the version string extracted from the output of the command execution. It includes extra information `'fish, version'` before the actual version number.
4. To fix the bug, we need to modify the code to extract only the version number from the output.
5. Update the code to strip the unnecessary part of the version string before formatting the output.

### Bug Fix
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split()[-1]  # Extract the actual version number
        return u'Fish Shell {}'.format(version)
``` 

After making this change, the function will correctly extract only the version number from the command output and return the expected output `'Fish Shell 3.5.9'`.