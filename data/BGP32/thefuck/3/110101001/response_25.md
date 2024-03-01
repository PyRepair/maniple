### Explanation:
The bug in the `info` function lies in the command used to get the Fish shell version. The command `'echo $FISH_VERSION'` does not return the version of Fish shell in the expected format.

### Bug Cause:
The failing test is expecting the output of `fish, version 3.5.9\n` but the function is currently using the command `'echo $FISH_VERSION'`, resulting in a mismatch.

### Strategy for Fixing the Bug:
Update the command used in the `Popen` call to retrieve the Fish shell version in the correct format.

### Corrected Version:
```python
# The corrected version of the buggy function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

By updating the command used to retrieve the Fish shell version to `['fish', '--version']`, the function will return the version in the correct format, fixing the bug.