The bug in the provided function lies in how the version string is extracted from the output of the `echo $FISH_VERSION` command. The current implementation includes a static string `Fish Shell` along with the extracted version, resulting in the incorrect output format.

### Cause of the bug:
The bug is caused by including the static string `'Fish Shell '` in the return statement, which does not match the expected output format.

### Strategy for fixing the bug:
To fix the bug, we should correctly extract the version string without including the static string in the return statement.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return version
```

By removing the static string `'Fish Shell '`, the corrected version of the function now returns only the extracted version string from the output of the `echo $FISH_VERSION` command. This satisfies the expected output format for the function.