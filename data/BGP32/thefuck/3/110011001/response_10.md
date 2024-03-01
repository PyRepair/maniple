### Analysis
- The `info` function is intended to retrieve the version of the Fish shell by executing a command using the `Popen` function.
- The expected output should be in the format `'Fish Shell x.x.x'`, but currently, it is incorrect due to an issue with parsing the version number.
- The error message indicates a mismatch between the expected output (`Fish Shell 3.5.9`) and the actual output (`Fish Shell fish, version 3.5.9`).

### Bug Cause
The bug is caused by directly reading the output of `Popen` without waiting for the process to complete and extract the correct version information.

### Bug Fix
To fix the bug, we need to wait for the subprocess created by `Popen` to complete before reading the output. Here's the corrected version of the function:

```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        proc.wait()  # Wait for the process to complete
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By adding `proc.wait()` before reading the output, we ensure that the process has completed execution before retrieving the version information, fixing the bug.