### Analysis:
The error message indicates that the output of the `shell.info()` function is not matching the expected value due to a discrepancy in the version string. The version retrieved from the `Popen` command includes extra characters (`'fish, version'`) which are not expected in the final output. This discrepancy causes the assertion error.

### Bug Cause:
The bug is caused by the incomplete extraction of the `FISH_VERSION` in the `info()` function. The `proc.stdout.read().decode('utf-8').strip()` method does not accurately filter out the unwanted characters in the version string fetched from the `Popen` command.

### Strategy for Fixing the Bug:
To fix this bug, it is necessary to correctly extract the version number from the output of the `Popen` command by removing the unwanted prefix (`'fish, version'`) and only capturing the version number. This can be achieved by using string manipulation methods to extract the version number substring accurately.

### Corrected Version of the Function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Get only the version number
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will now accurately extract the version number from the output and provide the expected output format `'Fish Shell 3.5.9'`. This updated version of the function should pass the failing test and resolve the reported issue on GitHub related to the incompatibility with Oh-My-Fish plugin.