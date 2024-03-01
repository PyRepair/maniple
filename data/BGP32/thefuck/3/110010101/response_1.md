### Analysis
1. The buggy function `info` in the `Fish` class is supposed to retrieve the version of the Fish shell and return it in a specific format.
2. The error message indicates that the function is returning the version string with extra text ('fish, version') before the actual version number.
3. The cause of the bug seems to be how the version information is being extracted from the stdout of the `Popen` process.
4. To fix the bug, we need to modify the way the version is extracted from the stdout to remove the extra text ('fish, version').

### Bug Fix Strategy
1. Extract the version part from the stdout response by splitting the string using the delimiter `,`.
2. Then strip any extra whitespace from the extracted version.

### Corrected Version

```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        
        version = output.split(',')[1].strip()  # Extract the version part and strip extra spaces
        return u'Fish Shell {}'.format(version)
```