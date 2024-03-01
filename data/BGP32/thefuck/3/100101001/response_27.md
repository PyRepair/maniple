### Bug Explanation
The buggy function is trying to capture the fish shell version by running the command `echo $FISH_VERSION`. However, the test is setting up the Popen mock with a different command `fish --version`, which is not being handled correctly in the buggy function. This mismatch causes the test to fail.

### Bug Fix Strategy
To fix the bug, we need to update the command being run by the Popen call in the `info` function to `fish --version` instead of `echo $FISH_VERSION`. This change will align the function with the expected behavior set by the test.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', ')[1]  # Extract only the version number
    return u'Fish Shell {}'.format(version)
```

By updating the command to `'fish', '--version'` and extracting only the version number from the output, the corrected function should now pass the failing test.