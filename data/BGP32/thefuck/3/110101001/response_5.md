### Bug Explanation
The bug arises from the incorrect command used to retrieve the Fish shell version in the `info` function. The function tries to get the Fish shell version by executing `echo $FISH_VERSION`, but the test is expecting the version to be retrieved using `fish --version`.

### Fix Strategy
To fix the bug, we need to update the command used to retrieve the Fish shell version to `fish --version`.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```