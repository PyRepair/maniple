## Fixing the Bug

### Error Analysis:
The `info` function in the `fish.py` file is trying to get the version of the Fish shell by executing the command `echo $FISH_VERSION`. However, in the failing test, the expected version is provided with a different format, causing the assertion error.

### Bug Cause:
- The `info` function returns the version of the Fish shell obtained by executing the wrong command.
- The failing test expects the version in a different format than what the function is currently returning.

### Proposed Fix:
Update the command executed in the `info` function to match the expected version format in the failing test.

### Updated `info` Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    raw_output = proc.stdout.read().decode('utf-8').strip()
    version = raw_output.split(',')[-1].strip()
    return f'Fish Shell {version}'
```

After applying this fix, the function will execute `fish --version` to fetch the correct version information.

This correction should make the function return the expected version format, resolving the failing test assertion error.