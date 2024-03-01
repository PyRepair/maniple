### Analysis
- The function `info` calls the `Popen` function from the `subprocess` module to execute a command that retrieves the Fish shell version.
- The error message indicates that the output of the command is not processed correctly, leading to an assertion error.
- The expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.
- The issue seems to be with how the version is extracted from the command output.

### Bug Cause
The bug is caused by not handling the output of the command properly. The expected version number '3.5.9' is part of the output 'fish, version 3.5.9', but the function is not processing it correctly.

### Fix Strategy
We need to modify the function to properly extract just the version number from the output of the command.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', ')[1]
    return u'Fish Shell {}'.format(version)
```

This corrected version reads the output of the command, splits it around the ', ' delimiter, and extracts the version number to ensure that only the version is returned.