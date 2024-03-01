### Cause of the Bug:
The bug in the `info` function lies in the incorrect command used to retrieve the Fish shell version. The command should be `echo $FISH_VERSION`, but the code is using `fish --version` instead.

### Strategy for Fixing the Bug:
To fix the bug, we need to update the command passed to `Popen` to `['fish', '-c', 'echo $FISH_VERSION']` instead of `['fish', '--version']`.

### Corrected Version of the Function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```