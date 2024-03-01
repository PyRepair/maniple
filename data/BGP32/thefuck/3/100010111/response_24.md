### Analysis
The error message indicates that the output from the `shell.info()` function does not match the expected value. The expected output is `'Fish Shell 3.5.9'` but the actual output is `'Fish Shell fish, version 3.5.9'`. This inconsistency suggests that the version string is not being extracted correctly in the buggy function.

### Error Location
The bug is likely occurring in the line where the version string is being extracted from the command output:
```python
version = proc.stdout.read().decode('utf-8').strip()
```
Here, the issue might be related to how the version information is read and decoded from the output of the `fish -c 'echo $FISH_VERSION'` command.

### Cause of the Bug
The bug is caused by the fact that the output read from the process is not being handled correctly, leading to the wrong version string being extracted and formatted.

### Strategy for Fixing the Bug
To fix this bug, we need to ensure that the version string is read and decoded correctly from the output of the `fish -c 'echo $FISH_VERSION'` command. This may involve modifying the way the data is read and processed.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.readline().decode('utf-8').split(",")[1].strip()
    return u'Fish Shell {}'.format(version)
```

In the corrected version:
- We read a single line of output using `proc.stdout.readline()`.
- We split the line by the comma `,` character to extract the version information.
- We strip any leading or trailing whitespace characters from the extracted version string.
- We format the extracted version string into the desired output format `'Fish Shell version'`.

This corrected version should properly extract the version information and format it as expected.