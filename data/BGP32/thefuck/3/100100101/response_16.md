### Analysis
- The `info` function is supposed to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` using the Popen function.
- The test expects the version to be extracted from the output `fish, version 3.5.9` and formatted as `'Fish Shell 3.5.9'`.
- The bug lies in the fact that the command used in the Popen call is `'fish', '-c', 'echo $FISH_VERSION'` instead of `'fish', '--version'`.
- This results in the incorrect extraction of the version in the buggy function.

### Bug Fix Strategy
To fix the bug, the Popen call should be modified to use the correct command `'fish', '--version'` so that the version is retrieved accurately.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return 'Fish Shell {}'.format(version)
```