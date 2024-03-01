The bug in the `info` function is caused by using the command `echo $FISH_VERSION` to retrieve the version of the Fish shell. The correct command to get the version is `fish --version`.

### Strategy for Fixing the Bug:
1. Update the command in the Popen call to `['fish', '--version']`.
2. Decode the output of the Popen process properly to get the version string.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]
    return 'Fish Shell {}'.format(version)
```