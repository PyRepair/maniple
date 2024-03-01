The bug in the provided function `info` is due to incorrect command execution that does not match the expected output format. The function is trying to retrieve the `FISH_VERSION` environment variable, but it is actually executing `echo $FISH_VERSION`. The test case expects the version number to be extracted correctly and formatted as `'Fish Shell X.X.X'`.

To fix the bug:
1. Change the command being executed to `['fish', '--version']` to ensure the correct version information is captured.
2. Adjust the text parsing to extract only the version number from the output.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version ')[1]
    return f'Fish Shell {version}'
```

This corrected version will properly extract the version number from the output of `fish --version` and format it as `'Fish Shell X.X.X'`.