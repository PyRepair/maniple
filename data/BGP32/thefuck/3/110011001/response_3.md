### Analysis:
- The error message indicates that the output of the `shell.info()` function does not match the expected output.
- The test input value for `version` is `'fish, version 3.5.9'`, but the function is expected to return `'Fish Shell 3.5.9'`.
- The code retrieves the version information using a subprocess call to the `fish` shell command and expects the format `'Fish Shell {version}'.

### Bug:
The bug in the code lies in how the version information is extracted from the subprocess output and formatted. The function is returning the raw output from the `echo $FISH_VERSION` command without converting it to the expected format.

### Fix:
To fix the bug, we need to extract only the version number from the output of the `fish` command and format it correctly.

### Corrected Version:
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()  # Extract version number
        return u'Fish Shell {}'.format(version)
```