### Analysis
The `info` function is attempting to get the version of the Fish shell by executing a command (`'echo $FISH_VERSION'`) in a subprocess and capturing the output. However, the issue lies in how the function is trying to read the output from the subprocess and format it.

### Bug
The bug occurs because the `proc.stdout.read()` method is being called before the process has finished executing, resulting in an empty string being read from the subprocess output.

### Fix
To fix this bug, we need to wait for the subprocess to complete before reading its output. This can be achieved by adding `proc.wait()` before attempting to read from `proc.stdout`.

### Corrected Version
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        proc.wait()  # Wait for the process to complete
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```