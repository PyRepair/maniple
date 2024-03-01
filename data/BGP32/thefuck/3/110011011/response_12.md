### Analysis
1. The buggy function `info` in the `Fish` class is attempting to retrieve the version of the Fish shell using a subprocess call to `fish -c 'echo $FISH_VERSION'`. The returned version is then formatted into a string.
2. The failing test is asserting that the expected output is `'Fish Shell 3.5.9'`, but the actual output contains the original version string before formatting.
3. Based on the runtime values provided, it seems that the subprocess mock is not returning the expected value for `proc.stdout.read()`. This causes the version string to not be properly extracted and formatted.
4. To fix the bug, the subprocess call should be mocked properly to return the expected version string.

### Fix Strategy
- Update the test setup to correctly mock the `Popen` call to return the desired version string.
- Ensure that the `stdout.read()` mock returns the correct value for the version.
- Modify the function to properly extract and format the version string.

### Corrected Version
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_raw = proc.stdout.read().decode('utf-8').strip()
        version = version_raw.split(',')[1].strip()  # Extract version number
        return u'Fish Shell {}'.format(version)
```

With this correction, the `info` function should now correctly extract the version of the Fish shell and format it into the expected string. This should resolve the failing test and the issue reported on GitHub regarding the Fish shell initialization with the Oh-My-Fish plugin.