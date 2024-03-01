## Bug Explanation
The issue in the `info` function is that the command being executed to get the Fish shell version is incorrect. The command `'echo $FISH_VERSION'` should actually be `'fish --version'` in order to retrieve the version information.

## Bug Fix
To fix the bug, we need to update the command being executed by `Popen` to `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

## Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
``` 

By changing the command to `['fish', '--version']` and then extracting the version from the output correctly, the function should now return the expected result and pass the failing test.