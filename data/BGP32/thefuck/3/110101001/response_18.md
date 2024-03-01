### Explain the cause of the bug
The bug in the `info` method of the `Fish` class lies in how the version of Fish shell is being retrieved. The method is using the command `echo $FISH_VERSION` to get the version, but the test is expecting the version to be retrieved using `fish --version`. This mismatch in the commands is causing the test to fail.

### Fix strategy
To fix the bug, we need to update the command used to retrieve the Fish shell version in the `info` method to be `fish --version`.

### Corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

By updating the command to `fish --version`, the corrected version of the function aligns with the expectation of the failing test.