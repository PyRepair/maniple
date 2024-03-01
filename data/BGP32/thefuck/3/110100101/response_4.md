### Analysis
The buggy function `info` is supposed to run a command to get the version of the Fish shell. However, the command `'fish', '-c', 'echo $FISH_VERSION'` is incorrect as it should be `'fish', '--version'` to get the version information correctly.

### Bug Explanation
The bug in the function `info` is caused by running the incorrect command to retrieve the version of the Fish shell. This leads to the version not being extracted correctly from the stdout of the process.

### Bug Fix
To fix the bug, simply change the command being run by `Popen` to `'fish', '--version'` instead of `'fish', '-c', 'echo $FISH_VERSION'`. This will correctly capture the version of the Fish shell.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```