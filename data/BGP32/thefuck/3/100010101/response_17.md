### Analysis
- The `info` function is attempting to get the version of the Fish shell by running a command using `Popen`.
- The error message shows that the function is returning `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`.
- The expected version is being printed as `'fish, version 3.5.9'` which is causing the assertion error.
- The variable `version` is not being extracted correctly from the command output.

### Bug cause
The bug is caused by not correctly extracting the version number from the output of the command `echo $FISH_VERSION`.

### Fix strategy
To fix the bug, the function should properly extract and format the version number from the command output before returning it.

### Corrected version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", version ")[1]  # Extracting version correctly
    return u'Fish Shell {}'.format(version)
```