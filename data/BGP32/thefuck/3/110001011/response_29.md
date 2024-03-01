### Analysis:
1. The `info` function is intended to return the name and version of the current shell, which in this case is the Fish shell.
2. The function uses `Popen` to execute a command `fish -c 'echo $FISH_VERSION'` to get the version of Fish shell.
3. The function reads the output of the command and formats it as `'Fish Shell {version}'`.
4. The issue reported on GitHub indicates that using `thefuck -v` causes a hang due to a recursive loop triggered by this `info` function.

### Identified Error:
The error is likely due to the fact that after executing `proc.stdout.read().decode('utf-8').strip()`, the `proc.stdout` is being read twice, which may lead to unexpected behavior. Additionally, it seems that the `DEVNULL` object is not imported correctly for handling stderr.

### Cause of the Bug:
When the function reads `proc.stdout` multiple times, it may not behave as expected, potentially leading to a hang or timeout issue. The incorrect import of `DEVNULL` may also cause unexpected behavior when handling stderr.

### Fix Strategy:
1. Import `DEVNULL` correctly.
2. Read the output of `Popen` only once to prevent any unexpected behavior.
3. Check for any potential issues related to reading stdout.

### Corrected Version:
```python
import os
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        stdout, _ = proc.communicate()
        version = stdout.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

By using `proc.communicate()` to get both stdout and stderr of the process and decoding `stdout` directly, we avoid any potential issues related to reading the output multiple times. The correct import of `DEVNULL` should ensure that stderr is properly handled.