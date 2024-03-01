### Bug Explanation
The buggy function `info` is trying to retrieve the fish shell version by running the command `echo $FISH_VERSION`. However, the test is expecting the version to be retrieved using the command `fish --version`, which is different from the actual command used in the function.

### Bug Fix
To fix the bug, we need to update the command in the `info` function to match what the test is expecting. Change `echo $FISH_VERSION` to `fish --version`.

### Corrected Version
```python
# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```