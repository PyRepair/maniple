Based on the provided information, the bug in the `info` function of the `Fish` class is caused by not properly handling the output of the `Popen` process when trying to get the Fish shell version. The output includes both the name `'fish'` and the version number, which causes the incorrect version to be displayed.

To fix this bug, we need to extract only the version number from the output and format the return statement accordingly. Here is the corrected version of the `info` function:

```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(' ')[-1]  # Extract version number from the output
        return u'Fish Shell {}'.format(version)
```

By extracting only the version number from the output of the `Popen` process, we ensure that the function returns the correct version of the Fish shell.

This correction aligns with the expected input/output values and resolves the issue mentioned on GitHub related to the recursive loop triggered by the incorrect handling of the shell version.