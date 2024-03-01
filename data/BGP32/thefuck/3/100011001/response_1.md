### Analysis
The error message states that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`. This indicates that the function is not correctly extracting the version number from the output of the shell command.

Looking at the runtime values, it seems that the `proc.stdout.read().decode('utf-8').strip()` expression is not correctly decoding the output of the shell command, leading to the inclusion of unwanted text in the version string.

### Bug Cause
The `proc.stdout.read().decode('utf-8').strip()` operation is not extracting the version number correctly from the output of the shell command. The incorrect decoding is causing additional text to be included in the version string.

### Fix
To fix the bug, we need to modify the way we extract the version number from the shell command output.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.readline().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

In the corrected version, we use `proc.stdout.readline().decode('utf-8').strip().split(',')[1].strip()` to extract the version number correctly by splitting the output at the comma and taking the second part. This should ensure that only the version number is included in the final output.