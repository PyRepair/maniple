### Analysis
The buggy function `info` is attempting to get the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'`. However, the way it is retrieving the version from the output is incorrect. The test is expecting a specific format for the version string, but the current implementation includes unnecessary text ("fish, version") along with the version number. This discrepancy causes the test to fail.

### Bug
The bug lies in how the version is extracted from the command output. The current implementation does not correctly remove the unnecessary text before the version number.

### Fix
To fix the bug, we need to modify the part of the code that extracts the version from the output to only include the version number. We can achieve this by splitting the version string and extracting the actual version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Split the version string to extract only the version number
    version_number = version.split(',')[1].strip().split()[1]
    return u'Fish Shell {}'.format(version_number)
```