### Analysis:
- The `info` function is attempting to retrieve the Fish shell version by executing the command `echo $FISH_VERSION`.
- The test function is checking if the retrieved version matches the expected format `'Fish Shell x.x.x'`.
- The error message indicates that the version retrieved includes additional content (`'fish, version'`) causing the assertion to fail.
- The GitHub issue suggests that the current implementation triggers a recursive loop causing the system to hang.

### Error Location:
- The issue lies in the command `'echo $FISH_VERSION'` not returning a clean version number due to the additional text in the output.

### Cause of the Bug:
- The `info` function retrieves the version of the Fish shell using the wrong command format, causing unwanted text (`'fish, version'`) to be included in the version string.

### Strategy for Fixing the Bug:
- Modify the command in the `Popen` call to use `'fish --version'` to retrieve the version with the correct format.
- Remove any unnecessary text parsing in `info` function to extract the version number cleanly.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[-1].strip()
    return u'Fish Shell {}'.format(version)
```

By making these changes, the `info` function should now correctly retrieve and format the Fish shell version.