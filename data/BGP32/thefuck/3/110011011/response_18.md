### Potential Error Locations:
1. The `Popen` call might not be capturing the correct output from the shell command.
2. The decoding of the output from `proc.stdout.read()` might not be working as expected.
3. The string formatting in the return statement might not be correct.

### Cause of the Bug:
The bug seems to be caused by the incorrect decoding of the output from the shell command. The `proc.stdout.read()` method is likely returning a bytes object that is not being decoded properly. This results in the version string being `'fish, version 3.5.9'` instead of just `'3.5.9'`. The extra information causes the assertion to fail.

### Strategy for Fixing the Bug:
1. Update the decoding of the output from `proc.stdout.read()` to ensure that only the version number is extracted.
2. Modify the string formatting in the return statement to concatenate 'Fish Shell' with the extracted version number.

### Corrected Version of the Function:
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_bytes = proc.stdout.read()
        version = version_bytes.decode('utf-8').strip().split(', ')[-1]  # Extracting only the version number
        return u'Fish Shell {}'.format(version)
``` 

After implementing this correction, the function should properly extract and return the version number, resolving the assertion failure in the test case.