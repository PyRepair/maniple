### Analysis
- The `info` function is supposed to retrieve the version of the Fish shell and return it in a specific format.
- The error message indicates that the returned version is not in the correct format.
- The test input simulates the output of `fish -c 'echo $FISH_VERSION'` as `b'fish, version 3.5.9\n'`, and the expected version is `'3.5.9'`.
- The bug seems to be related to how the version output is extracted from the command result and formatted in the return statement.

### Bug
The bug occurs when extracting the version from the command output. The current implementation does not correctly extract just the version string.

### Fix
To fix the bug, we need to modify how the version is extracted from the command output and format it correctly before returning.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split()[-1]  # Extract only the version string
    return u'Fish Shell {}'.format(version)
``` 

After making this correction, the function should correctly extract the version string and return it in the expected format, passing the failing test.