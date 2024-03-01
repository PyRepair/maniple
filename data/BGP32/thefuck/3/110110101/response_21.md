### Analysis
1. The buggy function `info` in the `Fish` class is not correctly reading the version of the Fish shell.
2. The test function calls the `info` function and expects the output to be `'Fish Shell 3.5.9'`.
3. The error message shows that the actual output includes unwanted text `'fish, version'` which is causing the assertion error.
4. The bug is likely in the way the output of the `Popen` command is processed to extract the version number.
5. The strategy for fixing the bug would involve correctly parsing the output of the `Popen` command to only extract the version number.

### Fix
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version_parts = version.split(' ')[-1]  # Extracting only the version number
        return 'Fish Shell {}'.format(version_parts)
``` 

The fixed version of the `info` function correctly parses the version number from the command output and returns it. This should now pass the failing test.