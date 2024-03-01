### Analysis
The buggy function `info` in `fish.py` is attempting to retrieve the version of Fish shell by running `echo $FISH_VERSION` command and extracting the output. However, in the failing test, the expected output is `'fish, version 3.5.9'`, which indicates that the command being executed is `'fish --version'`. This discrepancy between the expected command output and the actual command used in the function is the root cause of the bug.

### Bug Cause
The buggy function is using the incorrect command to retrieve the Fish shell version. Instead of `echo $FISH_VERSION`, it should be using `fish --version`.

### Fix Strategy
To fix the bug, update the command being executed from `echo $FISH_VERSION` to `fish --version` to properly fetch and extract the Fish shell version.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

This corrected version uses the correct command to fetch the Fish shell version and appropriately processes the output to extract the version number.