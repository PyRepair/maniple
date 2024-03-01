### Analysis
The buggy function `info()` in the `fish.py` file is attempting to extract the Fish Shell version using the command `echo $FISH_VERSION`. However, the failing test provides the version as `'fish, version 3.5.9\n'`, which includes the shell name as well. This discrepancy causes the test to fail. Additionally, the expected behavior is to return only the version number without the shell name.

### Bug Cause
The bug is caused by the mismatch between the expected version format ('3.5.9') and the actual version format ('fish, version 3.5.9\n'). This mismatch arises due to the function extracting the entire output without filtering out the unnecessary text.

### Strategy for Fixing the Bug
To fix the bug, we need to filter out only the version number from the output of the command. This can be achieved by parsing the output and extracting the version number portion before returning it.

### Corrected Version
The corrected version of the function `info()` in the `fish.py` file is as follows:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip().split(' ')[1]  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
```

By adding the necessary code to extract only the version number from the output, the function now correctly parses the version information and returns it without the shell name. This change ensures that the function passes the failing test and meets the expected behavior.