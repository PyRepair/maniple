### Analysis
The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the function is returning `'Fish Shell fish, version 3.5.9'`. This discrepancy likely stems from the way the version is being extracted from the output of the `fish -c 'echo $FISH_VERSION'` command.

Looking at the runtime values, we can see that the `version` variable is being set to `'fish, version 3.5.9'`. This suggests that the output of the command includes the string `'fish, version'`, which is not part of the desired version string.

### Cause of the Bug
The issue seems to be related to how the version is being extracted from the command output. The current implementation is simply reading the output as a string without parsing out the version number correctly.

### Fix Strategy
To fix this issue, we need to extract only the version number from the command output and construct the correct return string `'Fish Shell <version>'`.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```