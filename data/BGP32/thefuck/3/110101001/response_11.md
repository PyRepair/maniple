### Bug Explanation
The bug in the `info()` function is due to the incorrect command being used to retrieve the Fish shell version. The function is currently running `echo $FISH_VERSION` instead of `fish --version` to get the version information. This results in the version output being incorrect and failing the test.

### Bug Fix Strategy
To fix the bug, modify the command in the `Popen` call to `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

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