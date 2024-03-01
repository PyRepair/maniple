The bug in the `info` function lies in the command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` is incorrect, and it should be `fish --version` to get the correct version information.

### Cause of the bug:
- The function is using an incorrect command (`echo $FISH_VERSION`) to get the Fish shell version.
- This incorrect command results in the version string being retrieved in a different format than expected.

### Strategy to fix the bug:
- Modify the command in the `Popen` call to `fish --version` to get the correct version information.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', ')[1]
    return f'Fish Shell {version}'
```

By making this change, the function should now correctly retrieve the Fish shell version and pass the failing test.