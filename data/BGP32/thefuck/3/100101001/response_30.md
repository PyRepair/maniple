## Bug Analysis
The issue lies in the `info` function where the command `echo $FISH_VERSION` is used to retrieve the Fish shell version, but the test is expecting the version to be obtained using the command `fish --version`. This discrepancy in commands is causing the test to fail.

## Bug Fix
To fix the bug, we need to update the command used to retrieve the Fish shell version to `fish --version` instead of `echo $FISH_VERSIO`n.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By updating the command in the `Popen` call to `['fish', '--version']`, the function will now correctly retrieve the Fish shell version and pass the failing test.