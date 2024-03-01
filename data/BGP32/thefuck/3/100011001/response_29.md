### Analysis
The error message shows that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`. This indicates that the function is not correctly formatting the version retrieved from the shell command.

Looking at the runtime values, it seems that the `version` variable contains the string `'fish, version 3.5.9'`, which is not correctly formatted.

The bug is likely occurring because the function is not properly extracting just the version number from the output of the shell command.

### Bug Fix Strategy
To fix the bug, we need to extract only the version number from the output of the shell command before formatting it into the final output string.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
```