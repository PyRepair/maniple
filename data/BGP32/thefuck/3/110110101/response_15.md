### Analysis
1. The buggy function `info` in the `Fish` class is using the command `echo $FISH_VERSION` to get the version of the Fish shell, but the test is expecting the output of `fish --version`.
2. The test is currently mocking the output of `fish, version 3.5.9\n` but the function is not properly handling this output.
3. The error message indicates that the expected value is `'Fish Shell 3.5.9'` but the actual value is `'Fish Shell fish, version 3.5.9'`.

### Bug Cause
The buggy function is using the incorrect command to get the version of the Fish shell, causing a mismatch between the expected version and the actual output in the test.

### Fix Strategy
Change the command used in the `Popen` call to `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']` to correctly get the version of the Fish shell.

### Corrected Version
```python
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]
        return u'Fish Shell {}'.format(version)
``` 

By updating the `Popen` command to retrieve the version correctly using `['fish', '--version']` and extracting the version number from the output using `split(' ')[-1]`, the corrected function should now return the expected result.