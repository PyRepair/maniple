### Analysis
The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`. This suggests that the function is not correctly parsing the version number from the command output.

From the provided runtime values, we can see that the `version` variable is being set to `'fish, version 3.5.9'`, and this is not the desired format.

### Bug Cause
The bug is caused because the function is not correctly extracting the version number from the command output. It is directly taking the output of the command `echo $FISH_VERSION`, which includes unnecessary text (`'fish, version '`).

### Fix Strategy
To fix the bug, we need to extract only the version number from the output of the command and use that to build the desired output format.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Extract only the version number
    version_number = version.split()[-1]
    return u'Fish Shell {}'.format(version_number)
``` 

With this correction, we split the `version` string and extract the last element (the version number) to build the output in the correct format. This should resolve the issue and produce the expected output.