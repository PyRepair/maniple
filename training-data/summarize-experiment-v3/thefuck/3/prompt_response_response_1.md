## Bug Fix

The bug in the `info` function is caused by the incorrect command being used to retrieve the version of the Fish shell. To fix this bug, the command used to retrieve the version should be updated to correctly obtain the version information. Additionally, the output parsing should be adjusted to ensure that the version is extracted accurately.

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-v'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

In the corrected code, the command used in the `Popen` call has been updated to `['fish', '-v']` to obtain the version of the Fish shell. Additionally, the `version` variable is updated to extract the version information from the output using the `split()[-1]` method to retrieve the last element of the split string. This should accurately retrieve the version and resolve the discrepancy between the expected and actual output values.

This fix addresses the issue reported in the GitHub bug, ensuring that the `info` function in the Fish shell class of the `thefuck` package retrieves and returns the correct version of the shell.