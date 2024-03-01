### Bug Explanation
The bug in the `info` function lies in the command used to get the Fish shell version. The command `echo $FISH_VERSION` is being used instead of `fish --version`. This results in the incorrect version being retrieved from the process output and causes the test to fail.

### Fix Strategy
To fix the bug, we need to update the command used to get the Fish shell version to `fish --version`.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```