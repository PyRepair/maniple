The bug in the provided function `info()` is that the command to retrieve the Fish Shell version is incorrect. The command `'echo $FISH_VERSION'` used in `Popen(['fish', '-c', 'echo $FISH_VERSION'], ...)` should be changed to `'fish', '--version'` to get the correct version number.

### Bug Explanation:
- The original function is trying to get the Fish Shell version by using the command `'echo $FISH_VERSION'`, which is incorrect.
- The test function is expecting the output to be `'Fish Shell 3.5.9'`, but due to the wrong command, it receives `'Fish Shell fish, version 3.5.9'`.
- This discrepancy causes the assertion error.

### Strategy for Fixing the Bug:
- Update the command used in `Popen` to `['fish', '--version']` to correctly retrieve the Fish Shell version.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_info = proc.stdout.read().decode('utf-8').strip()
    version = version_info.split(", ")[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

By changing the command in `Popen` to `['fish', '--version']`, the function will correctly retrieve the Fish Shell version and pass the failing test.