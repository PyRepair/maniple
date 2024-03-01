### Analysis
The error occurs because the `shell.info()` function is returning the version string with the format `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`. This discrepancy is caused by the fact that the version string retrieved from the `Popen` process still contains the prefix `'fish,'`.

### Bug Fix Strategy
To fix this bug, we need to remove the `'fish,'` prefix from the version string before formatting it with the `'Fish Shell {}'` template.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.replace('fish, ', '')  # Remove 'fish,' prefix
    return u'Fish Shell {}'.format(version)
``` 

With this correction, the function will now correctly format the version string as `'Fish Shell 3.5.9'`, fixing the bug identified in the failing test.