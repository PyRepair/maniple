### Analysis:
1. The buggy function `info()` in the `Fish` class is supposed to return the name and version of the Fish shell, but it currently reads the version incorrectly.
2. The test function `test_info` simulates the call to `info()` and expects the output to match the version specified in the `side_effect`.
3. The cause of the bug lies in the incorrect command being used to retrieve the Fish shell version, leading to a mismatch in the expected and actual version values.
4. For fixing the bug, we need to update the command to retrieve the correct Fish shell version and decode it properly to get the desired output.

### Bug Fix:
```python
# The relative path of the corrected file: thefuck/shells/fish.py

from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.readline().decode('utf-8').strip()
        return 'Fish Shell {}'.format(version)
```

### Explanation:
1. Changed the command in `Popen` to `['fish', '--version']` to correctly obtain the Fish shell version.
2. Used `proc.stdout.readline()` to read the version line by line and decode it with `utf-8` encoding.
3. Updated the output format to match the expected output in the test function.
4. This correction ensures that the function `info()` fetches the Fish shell version correctly and returns it in the expected format.