### Bug Analysis
1. The buggy function `info` is trying to get the version of the Fish shell by running a command `echo $FISH_VERSION` and capturing the output. However, in the test code, the expected command being run is `fish --version`.
2. The expected output version is missing the `"fish, version"` prefix which is present in the actual output.
3. The error message indicates that the expected output is `'Fish Shell 3.5.9'` but the actual output includes the full command `'Fish Shell fish, version 3.5.9'`.

### Bug Location
The cause of the bug is due to the mismatch in the command used to retrieve the version and the mismatch in the expected output format.

### Bug Fix Strategy
To fix the bug, update the command used in the Popen call to `['fish', '--version']` to match the command `fish --version`. Also, modify the format string to strip out the unwanted prefix `fish, version` from the output.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')
    return u'Fish Shell {}'.format(version)
```