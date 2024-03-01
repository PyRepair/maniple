### Analysis
The buggy function `info()` is supposed to return the name and version of the Fish shell by executing a command in the shell. The issue seems to be with the handling of the command output and extracting the version number.

### Bug Cause
The bug seems to be caused by not properly decoding and stripping the output of the `Popen` command. The expected version number is `'3.5.9'`, but the current implementation includes extra text like `'fish, version '`.

### Fix Strategy
To fix the bug, we need to correctly decode the output of the `Popen` command and extract only the version number.

### Corrected Version
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.communicate()[0]  # Get the command output using communicate
        version = output.decode('utf-8').strip()  # Decode and strip the output
        return u'Fish Shell {}'.format(version.split(', version ')[1])  # Extract and return version number
```

This corrected version should properly extract the version number from the output of the `Popen` command and return it as expected.