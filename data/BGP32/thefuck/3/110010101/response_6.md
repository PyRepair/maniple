### Analysis
1. The `info` function in the `Fish` class is attempting to retrieve the version of the Fish shell by executing a command `echo $FISH_VERSION` using `Popen`. However, the function is not correctly extracting the version from the output.

2. The error is evident in the failing test message, which shows that the function is returning `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`. This indicates that the version extraction from the command output is incorrect.

3. The expected version string should be extracted from the output of the process and then formatted as `'Fish Shell version'`. The current implementation fails to extract and format the version correctly.

4. To fix the bug, we need to update the way the version is extracted from the process output using `stdout.read()`. We need to ensure that only the version number is extracted without any extra text.

### Bug Fix
```python
from subprocess import Popen, PIPE
from ...utils import DEVNULL, cache

class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()  # Read the entire output
        version = version.split(', version ')[1]  # Extract the version number
        return u'Fish Shell {}'.format(version)
```

With this fix, the function should correctly extract only the version number from the output of the process and format it as `'Fish Shell version'` before returning.