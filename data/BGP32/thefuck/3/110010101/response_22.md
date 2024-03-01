### Analysis
1. The buggy function `info` is supposed to return the name and version of the current shell by running the command `fish -c 'echo $FISH_VERSION'`. The bug seems to be related to how the version information is fetched and formatted.
2. The error message indicates that the version string retrieved includes extra characters like 'fish,' in addition to the actual version number.
3. The expected output is the string `'Fish Shell 3.5.9'`, but the function is returning a string with extra characters included.
4. The bug seems to be caused by the way the version string is manipulated after retrieving it from the `proc` variable. The format of the version string needs to be corrected.
5. To fix the bug, we need to remove any additional characters from the version string retrieved and ensure that the name of the shell ('Fish Shell') is included in the final output.

### Bug Fix
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()  # Read and decode version
        version = version.replace('fish, version ', '')  # Remove extra characters
        return u'Fish Shell {}'.format(version)  # Include the shell name before the version
``` 

Now the corrected `info` function should return the expected output `'Fish Shell 3.5.9'`.