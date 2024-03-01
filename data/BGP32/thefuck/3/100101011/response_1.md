### Analysis:
The `info` function in the `fish.py` file is trying to retrieve the Fish shell version using the command `'echo $FISH_VERSION'`, but the test case is expecting the version to be obtained using `'fish --version'`, leading to a mismatch in the output values.

### Error Location:
The error is in the command used to get the Fish shell version in the `info` function.

### Cause of the Bug:
The bug occurs because the `info` function is not using the correct command to retrieve the Fish shell version, causing the function to return the wrong version number. The discrepancy between the expected command in the test and the actual command used in the function leads to test failures.

### Fix Strategy:
To fix the bug, we need to update the command in the `info` function to `'fish --version'` to align with the test case expectations.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
```

With this correction, the `info` function will now use the correct command to retrieve the Fish shell version, resolving the discrepancy between the function's behavior and the test case expectations.