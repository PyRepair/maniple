### Cause of the bug:
The bug in the `info` function of the `Fish` class is due to the incorrect command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` does not return the correct version format, causing the function to fail when trying to extract and format the version.

### Strategy for fixing the bug:
To fix the bug, we need to correct the command used to retrieve the Fish shell version so that it provides the version in the expected format.

### Corrected version of the function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        # Updated command to retrieve the Fish shell version
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.readline().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split()[-1])
``` 

By updating the command to `['fish', '--version']` and modifying how the version is extracted from the output, the corrected `info` function should now properly return the Fish shell name and version.