### Analysis
- The buggy function is trying to get the version of the Fish shell by running a command using `Popen`.
- The error message indicates that the version retrieved includes additional text "fish, version".
- The expected version should only be the version number without the extra text "fish, version".

### Bug
The bug is occurring because the function is not correctly stripping out the extra text "fish, version" from the output.

### Fix
To fix the bug, we need to modify the process of retrieving the version number to exclude the extra text.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]  # Extract version number using split
    return u'Fish Shell {}'.format(version)
``` 

### Explanation
- In the corrected version, we added `.split(' ')[-1]` after stripping the output to get only the version number without the extra text.
- This modification ensures that only the version number is used when constructing the return string.