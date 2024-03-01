### Analysis
The issue in the `info` function seems to be related to how the output from the `Popen` subprocess is being read and decoded. It appears that the `proc.stdout.read()` method returns a MagicMock object instead of the actual output of the command. This might be the reason why the version variable is not correctly extracted.

### Bug Cause
The bug is likely caused by the use of `MagicMock` objects instead of the actual output from the subprocess. This results in the `version` variable being incorrect due to the decoding not working as expected.

### Fix Strategy
To fix this issue, we need to ensure that the `proc.stdout.read()` method returns the actual output of the command being executed. This can be achieved by waiting for the subprocess to finish and collecting its output properly.

### Corrected Version
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        proc.wait()  # Wait for the subprocess to finish
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

By adding `proc.wait()` before reading the output, we ensure that the subprocess finishes execution before reading its output. This should fix the issue related to incorrect output and decoding.