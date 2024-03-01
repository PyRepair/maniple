### Analyze the Bug

1. **Buggy Function and Class Relationship**:
   - The buggy function `info` is a method of the `Fish` class, responsible for returning the name and version of the current shell.

2. **Error Location**:
   - The error seems to be related to the incorrect parsing of the version string retrieved from the shell.

3. **Bug Cause**:
   - The buggy function is reading the output of the command incorrectly, leading to an incorrect version format.
   - The failing test expects the version string to be 'Fish Shell 3.5.9' but encounters 'Fish Shell fish, version 3.5.9'.

4. **Bug Fix Strategy**:
   - Modify the way the version string is extracted from the command output to match the expected format.

### Corrected Version of the Buggy Function

```python
# The corrected version of the buggy function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
    return u'Fish Shell {}'.format(version)
```

### Changes Made:
- Updated the command in `Popen` to `['fish', '--version']` to correctly fetch the Fish Shell version.
- Modified the extraction of the version from the output to only retrieve the version number without extra text.

By making these changes, the corrected version of the function should now return the version string in the expected format, resolving the failing test case.