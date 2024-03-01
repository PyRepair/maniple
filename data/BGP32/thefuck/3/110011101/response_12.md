The bug in the provided function is due to the incorrect formatting of the version output obtained from the subprocess. The `info` function is extracting the version with additional text, which causes the assertion to fail when comparing the actual output with the expected one.

To fix this bug, you need to modify the way the version is extracted so that only the version number is considered. You can achieve this by splitting the output string and getting only the version number part.

Here is the corrected version of the `info` function:

```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(',')[1].split()[1]
        return 'Fish Shell {}'.format(version)
```

With this correction, the function will properly extract and format the version number without including unnecessary text. This should make the failing test pass with the expected output 'Fish Shell 3.5.9'.