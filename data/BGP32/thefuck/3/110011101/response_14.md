### Analysis
The bug in the provided function is due to the fact that the version string extracted from the command output includes unnecessary information ("fish, version"). This causes the assertion to fail as the expected output does not contain the extra information.

### Bug Fix Strategy
To fix the bug, we need to modify the code to extract only the version number from the output string. We can achieve this by splitting the output string based on spaces and selecting the last element, which should be the version number.

### Corrected Version

```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```

With this correction, the function will correctly extract the version number from the command output and return the expected result.