### Analysis
The failing test is expecting the output of the `info` function to be `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`. This discrepancy is due to the version information being read from the subprocess output but not correctly formatted in the return value.

### Bug Cause
The bug is caused by not properly processing the version information retrieved from the subprocess output. The version string still contains the extra `'fish, version '` text which needs to be removed.

### Fix
To fix the bug, we need to extract the version number from the retrieved string and format the return value accordingly before returning it.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```