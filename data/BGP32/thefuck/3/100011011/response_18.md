### Identified Bug:
The bug stems from the fact that the `info` function is extracting the Fish version string incorrectly from the output of the subprocess. The expected version string is `'Fish Shell 3.5.9'`, but the actual output from the subprocess is `'fish, version 3.5.9'`. This leads to the assertion error because the two strings do not match.

### Bug Cause:
The cause of the bug is that the extraction of the version string from the subprocess output is not being handled correctly. The subprocess output includes additional information (`'fish, version'`) before the actual version number. This discrepancy causes the version comparison to fail.

### Fix Strategy:
To fix the bug, we need to properly extract and format the version string so that it matches the expected format `'Fish Shell X.X.X'`. We can achieve this by splitting the subprocess output based on the comma and space, then taking the last element of the resulting list as the version number.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_info = proc.stdout.read().decode('utf-8').strip()
    version = version_info.split(', ')[-1]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will properly extract the version number and format it as `'Fish Shell X.X.X'`, aligning it with the expected output `'Fish Shell 3.5.9'`.