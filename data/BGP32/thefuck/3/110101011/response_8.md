The bug in the provided function `info()` is due to the incorrect command used to retrieve the Fish shell version. The function is using `echo $FISH_VERSION`, but the test expects the version to be obtained using `fish --version`.

### Explanation of the Bug:
- The function `info()` is using the command `echo $FISH_VERSION` to get the Fish shell version.
- However, the test function is expecting the version to be retrieved by running `fish --version`.
- This inconsistency in the commands causes the function to return an incorrect version string, leading to the failing test.

### Strategy for Fixing the Bug:
To fix the bug, we need to update the command used to retrieve the Fish shell version in the `info()` function. We should modify it to use `fish --version` instead of `echo $FISH_VERSION`.

### Corrected Version of the Function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By updating the command to use `fish --version`, the corrected function will now return the correct version string, resolving the issue and passing the failing test.