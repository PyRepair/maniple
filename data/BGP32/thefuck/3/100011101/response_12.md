### Analysis:
- The error message indicates that the function is returning the shell version with an additional "fish, " prefix.
- The expected output does not contain the "fish, " prefix, but only the version number.
- This discrepancy suggests that the issue lies in how the version string is being processed.

### Bug Cause:
- The bug is caused by the function including the entire string returned by the command, which includes the "fish, " prefix, instead of just extracting the version number.

### Fix Strategy:
- To fix the bug, we need to modify the function to only extract the version number from the string returned by the command.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

The corrected version of the function splits the version string by spaces and extracts the last element, which should be the version number only, effectively removing the unnecessary "fish, " prefix.