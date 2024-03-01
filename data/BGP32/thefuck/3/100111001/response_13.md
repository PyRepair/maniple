### Analysis
The bug in the `info` function lies in the command being used to retrieve the Fish shell version. The function is currently executing `echo $FISH_VERSION` to get the version, but the test is expecting the version to be retrieved using `fish --version`.

### Bug Cause
1. The `Popen` call in the `info` function is using the command `echo $FISH_VERSION`, which does not return the version string in the required format.
2. The test function is setting the expected output based on the version retrieved using `fish --version`, which is incorrect due to the different command being used in the `info` function.

### Fix Strategy
To fix this bug, we need to update the command being executed in the `Popen` call to `fish --version` to correctly retrieve the Fish shell version string.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(', version ')[1])
``` 

This corrected version of the function uses the correct command `fish --version` to retrieve the version string. It then extracts the version number from the output using `split`, assuming the version format remains consistent.