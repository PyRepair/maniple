### Analysis:
The buggy function `info` is supposed to extract the version of the Fish shell by running a command in the shell. However, in the test function, the expected version string `3.5.9` does not match the actual extracted version `fish, version 3.5.9`.

### Bug:
The bug lies in how the function extracts and processes the version string from the output of the command. The function is expecting to receive only the version number, but it is receiving additional information such as `'fish, version'` along with the version number.

### Fix:
To fix the bug, we need to modify the function to properly extract the version number from the command output and discard the unnecessary text.

### Corrected Version:

```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

After making this correction, the function should now properly extract and return just the version number from the output, satisfying the test case.