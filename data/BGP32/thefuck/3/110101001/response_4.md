### Explanation:
The buggy function `info` is attempting to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` using the `Popen` function. However, in the failing test, the expected output of the command is `fish, version 3.5.9\n`, which does not match the expected format `3.5.9` in the assert statement. This mismatch is causing the test to fail.

### Bug:
The bug lies in the way the `info` function is trying to extract the Fish shell version from the output of the command. It is not correctly parsing the version number from the command output.

### Strategy for fixing the bug:
To fix the bug, we need to extract the correct version number from the command output. This can be achieved by updating the way the version is retrieved from the output of the `Popen` command.

### Corrected Version:
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()  # Read version output
        version_number = version.split(',')[1].strip()  # Extract version number
        return u'Fish Shell {}'.format(version_number)
```

By updating the command to `['fish', '--version']` and extracting the version number correctly from the output, the corrected version of the `info` function should now be able to pass the failing test.