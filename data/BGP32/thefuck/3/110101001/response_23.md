### Bug Explanation
The bug in the `info` function arises from the fact that the command being executed is `echo $FISH_VERSION`, but the test is expecting the version to be retrieved using `fish --version`. This discrepancy causes the test to fail as the expected command output does not match the actual output obtained by the function.

### Bug Fix Strategy
To fix the bug, we need to modify the command executed by `Popen` to be `fish --version` instead of `echo $FISH_VERSION`. This will ensure that the correct version information is retrieved and compared with the expected value in the test.

### Corrected Version
```python
# The corrected version of the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```