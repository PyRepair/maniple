### Bug Explanation
The bug in the `info` function is caused by the incorrect command used to retrieve the version of the Fish shell. The function is calling `echo $FISH_VERSION` instead of `fish --version` to get the shell version. This results in the incorrect version string being extracted from the command output, which leads to the failing test.

### Fix Strategy
To fix the bug in the `info` function, we need to modify the command passed to `Popen` to `fish --version` so that it retrieves the correct version string.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(", ")[1]
        return u'Fish Shell {}'.format(version)
``` 

After implementing the above corrected version, the test case should pass successfully.