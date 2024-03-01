### Analysis
The error message indicates that the function `info()` is returning the incorrect version string `'fish, version 3.5.9'` instead of `'3.5.9'`. This discrepancy causes the assertion error in the test.

The issue on GitHub suggests that the problem is related to the specific format of the version returned by the Fish shell command.

### Bug Cause
The bug is caused by the fact that the command `echo $FISH_VERSION` is returning more than just the version number, it is also returning the label `'fish, version'` alongside the version number. This extra information is not desired and leads to the incorrect output.

### Fix Strategy
To fix the bug, we need to modify the way we extract the version number from the shell command output. We should extract only the version number itself by considering the format in which the version is returned by the Fish shell.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]  # Extracting just the version number
    return u'Fish Shell {}'.format(version)
```

With this modification, only the version number is extracted from the command output, which should now match the expected output `'3.5.9'`.