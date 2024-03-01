### Analysis
The `info` function in the `Fish` class is intended to return the version of the Fish shell in a specific format. However, the bug is causing it to return the version in an incorrect format.

### Bug
The bug lies in how the version information is being extracted from the `stdout` of the `Popen` process. The function is not correctly decoding the output to get the version and is returning the raw output instead.

### Fix
To fix the bug, we need to properly decode the output from `stdout` before constructing the return string.

### Corrected Version
```python
# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(',')[1].strip().replace('version', '')
        return u'Fish Shell {}'.format(version)
``` 

This corrected version correctly extracts the version from the stdout and formats it appropriately before returning the final string.