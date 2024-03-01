### Analysis
The bug in the `info` function is caused by the incorrect command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` is being used instead of `fish --version`. Additionally, the expected output in the failing test is `'fish, version 3.5.9\n'` but the function is trying to strip just the version number, resulting in the incorrect output.

### Bug Fix Strategy
1. Change the command in the `Popen` call to `'fish', '--version'` to correctly get the Fish shell version.
2. Update the parsing of the version number to correctly extract the version value from the output.

### Bug-fixed Version
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
```