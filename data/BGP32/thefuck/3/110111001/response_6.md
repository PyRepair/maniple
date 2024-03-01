### Analysis
1. In the `info()` function, the command `echo $FISH_VERSION` is used to retrieve the version of the Fish shell.
2. The test is expecting the version string to be in the format `3.5.9`, but the actual output includes unnecessary text (`fish, version`).
3. The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.
4. The discrepancy is caused by the incomplete parsing of the version string, which includes extra information that needs to be removed.
5. To fix the bug, we need to extract only the version number from the output string and format it correctly before returning the shell name and version.

### Bug Fix
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```

By splitting the version string and extracting the last element (which should be the version number), we can ensure that only the version is included in the output. This fix should address the bug and make the test pass successfully.