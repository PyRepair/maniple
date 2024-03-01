### Analysis
The buggy function `info` is attempting to retrieve the version of the Fish shell by running a command using `Popen`. However, the issue lies in how the function is reading the output from the process. The `proc.stdout.read()` method is not correctly handling the process output, resulting in an incorrect `version` value being extracted.

### Bug Cause
The bug is caused by not handling the process output properly when trying to read the version of Fish shell. Instead of directly reading the output using `proc.stdout.read()`, we should use `communicate()` method to get the output and error streams.

### Strategy for Fixing the Bug
We need to modify the way the output from the process is read in order to correctly capture the version of the Fish shell. By using the `communicate()` method, we can ensure that we capture the complete output of the process.

### Corrected Version
```python
# Importing necessary module
from subprocess import Popen, PIPE

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        out, _ = proc.communicate()
        version = out.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```