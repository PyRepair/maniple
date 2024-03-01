### Analysis
1. **Buggy Function**: The `info` function in the `Fish` class is supposed to retrieve the version of the Fish shell. However, the command to fetch the version (`echo $FISH_VERSION`) is incorrect.
   
2. **Test Code**: The test code is mocking the `Popen` object and setting up a side effect for `stdout.read` to return the string `'fish, version 3.5.9\n'`.

3. **Error Message**: The assertion error occurs because the expected output is `'Fish Shell 3.5.9'` while the actual output includes extra text (`'fish, version'`).

### Bug Cause
The buggy function is retrieving the version incorrectly, which results in the unexpected string format (`'fish, version 3.5.9'`). The actual output doesn't match the expected output due to this issue.

### Fix Strategy
Modify the command passed in `Popen` to `fish --version` in order to get the correct version string that matches the expected format.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split()[-1])
```

By using `fish --version` instead of `echo $FISH_VERSION`, the function should now correctly retrieve the version as expected.