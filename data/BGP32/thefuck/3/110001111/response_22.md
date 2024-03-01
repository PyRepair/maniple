Based on the provided information, the bug in the `info` function of the `Fish` class is caused by not closing the `proc` process after executing the command to get the Fish version. This leads to the hanging issue described in the GitHub problem where the plugin triggers a recursive loop.

To fix this bug, it is necessary to wait for the process to finish and then close it properly before reading the output. Also, the output should only include the version number without any additional text.

Here is the corrected version of the `info` function:

```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.communicate()[0].decode('utf-8').strip()
        proc.wait()
        proc.stdout.close()
        proc.stderr.close()
        return u'Fish Shell {}'.format(version.split()[-1])
```

This version correctly waits for the process to finish, fetches the output, closes the process, and returns only the version number without any additional text. This should resolve the hanging issue described in the GitHub problem.