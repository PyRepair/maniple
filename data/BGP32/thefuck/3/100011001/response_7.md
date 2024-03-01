### Bug Analysis:
The error message shows that the `info()` function is returning `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`. This indicates that the version string retrieved from the shell command includes extra text (`'fish, version '`).

### Bug Location:
The bug is likely located in the line where the version is extracted from the output of the shell command. The `proc.stdout.read().decode('utf-8').strip()` operation is not correctly extracting only the version number.

### Bug Cause:
The `echo $FISH_VERSION` command in the shell is returning a string that includes the text `'fish, version '` along with the actual version number. This extra text is causing the version string to be incorrect.

### Fix Strategy:
To fix the bug, we need to modify the way we extract the version number from the shell command output. We should strip the extra text `'fish, version '` from the version string and only keep the actual version number.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')
    return u'Fish Shell {}'.format(version)
```