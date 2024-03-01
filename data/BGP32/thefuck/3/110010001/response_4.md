## Analysis
1. The buggy function is `info` within the `Fish` class in the `fish.py` file.
2. The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.
3. The cause of the bug is that the format of the version string retrieved from the subprocess is not correct due to the incorrect string manipulation.
4. To fix the bug, we need to properly extract only the version number part of the output string.
5. I will modify the function to correctly extract the version number.

## Corrected Version
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        version = version_output.split(',')[1].strip()  # Extract version part after the comma
        return u'Fish Shell {}'.format(version)
```

By splitting the version string using the comma as a separator and taking the second part, we ensure that only the version number is extracted and used in forming the correct output format.