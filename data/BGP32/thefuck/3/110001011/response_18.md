### Identified Bug:
The `info` function in the `Fish` class is attempting to retrieve the Fish shell version by running the command `fish -c 'echo $FISH_VERSION'` using `Popen`. However, the function is not properly capturing the output from the `Popen` process, leading to incorrect behavior.

### Explanation of the Bug:
The bug is likely caused by not properly handling the process output from `Popen`. The `Popen` object needs to be communicated with properly to get the correct output from the command execution.

### Fix Strategy:
Modify the code to properly handle the output from the `Popen` process by using `communicate()` to properly capture the output and avoid any potential hanging.

### Corrected Version of the Function:
```python
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

By using `proc.communicate()`, we properly capture the output from the `Popen` process and decode it to get the correct version of the Fish shell. This should resolve the issue of hanging during the shell initialization with the Oh-My-Fish plugin.