### Analysis
- The error message shows that the function is returning a string with unnecessary additional text (`'fish, version'`).
- The expected output is `'Fish Shell 3.5.9'`.
- The function is attempting to get the version of the Fish shell using the command `'echo $FISH_VERSION'`, which returns `'fish, version 3.5.9\n'`.
- The function needs to extract only the version number from the output.

### Bug Fix Strategy
- The bug is caused by the incorrect parsing of the version output from the command.
- To fix the bug, we need to extract only the version number from the output and remove any unwanted text.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split()[2].rstrip('\n')
    return u'Fish Shell {}'.format(version)
``` 

This corrected version of the `info` function should now correctly extract and return only the version number without the unnecessary text.