### Analysis
The error message indicates that the output received from the `proc.stdout.read().decode('utf-8').strip()` operation is not as expected. The expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.

### Bug Cause
The issue with the buggy function is that it is not correctly parsing the version string obtained from the command `echo $FISH_VERSION`. The function is directly using the output without properly extracting the version number.

### Fix Strategy
To fix this bug, we need to extract only the version number from the output of the `echo $FISH_VERSION` command. We can do this by splitting the output string and extracting the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()  # Extracting version number from the output
    return u'Fish Shell {}'.format(version)
``` 

This corrected version of the function should properly extract the version number from the output and return `'Fish Shell 3.5.9'` as expected.