### Potential Error Locations
1. The `read` function used on `proc.stdout` may not be reading the correct output.
2. The way the `version` is extracted from the output may not be handling the string properly.

### Bug Cause
The bug is caused by the fact that the `info` function in the `Fish` class is not correctly extracting the version number from the output of the `fish -c 'echo $FISH_VERSION'` command. The function then appends the output string as is without properly extracting the version number.

### Strategy for Fixing the Bug
1. You need to ensure that the `version` is correctly extracted from the output of the command.
2. Strip any unwanted characters from the extracted version number before formatting it into the output string.

### Corrected Version of the Function
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extract only the version number from the output
        version = version.split(" ")[-1]
        return u'Fish Shell {}'.format(version)
```

By splitting the output and taking only the last element as the version number, the corrected function should now extract the correct version number from the output. This should resolve the failing test issue.