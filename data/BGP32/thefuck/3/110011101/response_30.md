Based on the provided information, the bug seems to be caused by the incorrect parsing of the version string retrieved from the shell command. The function is extracting the version information including unnecessary characters like 'fish, version' instead of just the version number.

To fix the bug, the function needs to properly parse the version string to only extract the version number.

Here is the corrected version of the function:

```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(', version ')[1]  # Extract just the version number
        return u'Fish Shell {}'.format(version)
```

This corrected version splits the output string to extract only the version number. This change should make the function return the expected output 'Fish Shell 3.5.9' as required by the failing test case.