### Bug Explanation
The bug lies in the command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` is used but it should be `fish --version` to correctly get the Fish shell version.

### Fix Strategy
Replace the command `echo $FISH_VERSION` with `fish --version` to ensure the correct version of the Fish shell is fetched.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```