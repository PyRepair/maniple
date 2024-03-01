### Fixing the bug

#### Explanation:
The bug in the `info` function of the `Fish` class lies in the command used to retrieve the version of Fish shell. The expected version format is `3.5.9` but the command `echo $FISH_VERSION` returns a string including `fish, version ` which needs to be extracted.

#### Strategy for Fixing the Bug:
1. Modify the command executed by Popen to isolate and return only the version number of Fish shell.
2. Update the return statement to incorporate the extracted version.

#### Corrected Version:
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION | cut -d " " -f 3'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By using the `cut` command in the `fish` shell with `-d " "` delimiter, we can isolate the version number and `f 3` to extract the third field which contains the version number only. This corrected version should now return the version number in the expected format.