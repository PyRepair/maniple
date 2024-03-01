### Analysis:
- The buggy function `info` is trying to retrieve the version of the Fish shell by executing a shell command and capturing the output.
- The issue lies in how the version string is being processed and returned back.
- The `version` variable is being set to the output of `proc.stdout.read().decode('utf-8').strip()`, which includes the shell name "fish, version" along with the actual version number.
- The expected output only requires the version number without the shell name prefix.

### Bug:
The `info` function is returning a version string that includes the shell name "Fish Shell" along with the version number, while it is expected to return only the version number.

### Fix:
1. Update the line where the `version` variable is assigned to extract only the version number without the shell name prefix.
2. Modify the return statement to return the version number appended with "Fish Shell".

### Corrected Version:
```python
# The corrected version of the info function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(" ")[-1]
    return u'Fish Shell {}'.format(version)
```