### Analysis
- The buggy function is attempting to retrieve the version of the Fish shell by running a command and reading the output.
- The bug is caused by the fact that the function includes the entire output string "fish, version 3.5.9" instead of only extracting the version number "3.5.9".
- This discrepancy between the expected and actual values causes the assertion error in the failing test.

### Bug Fix Strategy
To fix the bug, we need to modify the function to extract only the version number from the retrieved output string.

### The corrected version of the function
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()  # Extract only the version number
        return u'Fish Shell {}'.format(version)
``` 

After applying this correction, the function should now correctly extract and return only the version number from the output.