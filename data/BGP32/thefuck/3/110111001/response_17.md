The buggy function `info` in the `Fish` class is attempting to read the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'` and capturing the output. However, it seems to be comparing the full output string (`'fish, version 3.5.9'`) instead of extracting just the version number (`3.5.9`) for comparison with the expected value.

### Bug Cause:
The bug occurs because the function `info` is not correctly parsing the version number from the command output before constructing the final string for return.

### Fix Strategy:
1. Update the code to extract only the version number from the command output.
2. Ensure that the extracted version number is compared with the expected value.

### Corrected Version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version_number = version.split(',')[1].strip().split()[-1]
    return u'Fish Shell {}'.format(version_number)
```

With this corrected version, the function will properly parse the version number and construct the output string for comparison. It should pass the failing test by correctly returning `'Fish Shell 3.5.9'`.