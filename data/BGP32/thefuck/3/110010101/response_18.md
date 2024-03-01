### Analysis
- The `info` function in the `Fish` class is supposed to obtain the version of the Fish shell by running a command in a subprocess and then return a formatted string with the version.
- The error message indicates that the expected output is `'Fish Shell 3.5.9'` but the actual output includes extra text like `'fish, version'`.
- The bug seems to be related to how the version information is extracted and formatted.

### Bug
The bug is caused by directly reading the output of the subprocess command without correctly parsing and extracting the version number from it. This leads to the unnecessary text `'fish, version'` included in the final output.

### Fix
To fix the bug, we need to extract only the version number from the output of the subprocess command and then format it correctly to match the expected output.

### Corrected Version
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

With this corrected version, the `info` function should correctly extract only the version number from the output of the subprocess command and return the formatted string `'Fish Shell 3.5.9'` as expected.