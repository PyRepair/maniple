To address the bug in the given function `info` within the `Fish` class, we need to correct the command used to retrieve the Fish shell version. The existing command `echo $FISH_VERSION` is incorrect as it retrieves the environment variable `FISH_VERSION` rather than the actual shell version. 

We need to change the command sent to the `Popen` function to `['fish', '--version']` to correctly retrieve the Fish shell version.

Here is the corrected version of the `info` function:
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split()[-1])  # Extracting the version number from the output

# Test function will now pass after this correction
```

By making this change, the function will now correctly retrieve and format the Fish shell version, resolving the bug and allowing the test to pass as expected.