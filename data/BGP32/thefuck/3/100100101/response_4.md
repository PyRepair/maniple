### Analysis
The buggy function `info` is supposed to return the version of the Fish shell by executing a command using `Popen`. However, the command `'echo $FISH_VERSION'` is different from the command used in the test `'fish, version 3.5.9\n'`. Also, the test checks for the command `['fish', '--version']`, which is not being used in the buggy function.

### Bug
1. The command used to get the version in the function is incorrect.
2. The test expects a different command `['fish', '--version']` which is not in the function.

### Fix
1. Change the command in the `Popen` call to `'fish --version'` to match the test's expected command.
2. Update the `.strip()` in the version retrieval to remove unwanted characters like commas and newlines.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')
    return u'Fish Shell {}'.format(version)
``` 

After applying this fix, the corrected function should pass the failing test and return the expected version string.