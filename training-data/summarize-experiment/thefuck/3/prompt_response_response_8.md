Based on the test case and error message, it seems that the issue lies with the `info` function in the `Fish` class. The `info` function is expected to return the name and version of the current shell, but it is currently returning a string that includes the entire output of the command, instead of just the version number.

The bug occurred because the `info` function is not correctly parsing the output of the command to extract only the version number. This results in the returned string containing unnecessary information.

To fix this issue, we need to modify the `info` function to extract only the version number from the command output and return the properly formatted string.

Here's the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(' ')[-1]  # Extract only the version number
    return u'Fish Shell {}'.format(version)
```

In this revised version, we have updated the command to `['fish', '--version']` to explicitly fetch the version information. We then extract only the version number from the output and return the properly formatted string.

This fix ensures that the `info` function returns the expected output and resolves the issue observed in the test case.