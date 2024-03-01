### Analysis:
- The `info` function is attempting to fetch the Fish Shell version using a subprocess call to the `fish` command with the parameter `-c 'echo $FISH_VERSION'`.
- The test is providing a side effect of `b'fish, version 3.5.9\n'` for `Popen.return_value.stdout.read`.
- The assertion error occurs because the function is returning `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`.
- The issue seems to be with the format of the version retrieved from the subprocess call.

### Bug:
The bug is in how the version string is formatted before returning it. The version string includes unnecessary text like "fish, version", which should be removed to match the expected output.

### Fix:
1. Extract only the version number from the retrieved string.
2. Use the extracted version number to format the output string.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version_number = version.split(' ')[-1]  # Extract only the version number
    return u'Fish Shell {}'.format(version_number)
```